from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Optional, Tuple
from urllib.parse import urlparse

PACKAGE_NAME = "from2to"
DEFAULT_STYLE = "new"


def is_url(text: str) -> bool:
    try:
        p = urlparse(text)
        return p.scheme in {"http", "https"}
    except Exception:
        return False


def get_package_root() -> Path:
    # Resolve to the installed package directory on the filesystem
    return Path(__file__).resolve().parent


def get_default_cache_dir() -> Path:
    # Prefer a cache dir inside the package install directory
    pkg_root = get_package_root()
    pkg_cache = pkg_root / "styles" / "cache"
    try:
        pkg_cache.mkdir(parents=True, exist_ok=True)
        test_file = pkg_cache / ".write_test"
        test_file.write_text("ok", encoding="utf-8")
        try:
            test_file.unlink()
        except Exception:
            pass
        return pkg_cache
    except Exception:
        pass

    # Fall back to user cache dirs
    import os

    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
    else:
        base = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))
    dir_ = Path(base) / PACKAGE_NAME
    dir_.mkdir(parents=True, exist_ok=True)
    return dir_


def list_included_styles() -> Iterable[str]:
    root = get_package_root() / "styles" / "included"
    if root.exists():
        for p in sorted(root.glob("*.css")):
            yield p.name


def list_cached_styles(cache_dir: Optional[Path] = None) -> Iterable[str]:
    cdir = cache_dir or get_default_cache_dir()
    if cdir.exists():
        for p in sorted(cdir.glob("*.css")):
            yield p.name


def download_url(url: str, dest: Path) -> None:
    import urllib.request

    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def resolve_style(
    style: str,
    *,
    cache_dir: Optional[Path] = None,
    no_cache: bool = False,
) -> Tuple[str, Optional[Path]]:
    """Resolve style to CSS text and origin path.

    Resolution order:
    - If URL: download to cache dir (unless no_cache -> temp) and use it.
    - Elif local path exists: use it.
    - Elif exists in cache dir as {style} or {style}.css: use it.
    - Elif exists in included styles as {style} or {style}.css: use it.

    Returns (css_text, origin_path)
    """
    cdir = cache_dir or get_default_cache_dir()

    def read_css(path: Path) -> str:
        return path.read_text(encoding="utf-8")

    if is_url(style):
        url_path = urlparse(style).path
        name = Path(url_path).name or "style.css"
        if not name.endswith(".css"):
            name = f"{name}.css"
        if no_cache:
            tmp = Path(tempfile.gettempdir()) / f"{PACKAGE_NAME}-{name}"
            download_url(style, tmp)
            return (read_css(tmp), tmp)
        else:
            cdir.mkdir(parents=True, exist_ok=True)
            target = cdir / name
            if not target.exists():
                download_url(style, target)
            return (read_css(target), target)

    p = Path(style)
    if p.is_file():
        return (read_css(p), p.resolve())

    names = [style]
    if not style.endswith(".css"):
        names.append(f"{style}.css")

    for nm in names:
        cp = cdir / nm
        if cp.is_file():
            return (read_css(cp), cp)

    inc_root = get_package_root() / "styles" / "included"
    for nm in names:
        ip = inc_root / nm
        if ip.is_file():
            return (read_css(ip), ip)

    raise FileNotFoundError(
        f"Could not resolve style '{style}'. Use URL, file path, cached name, or included name."
    )


def inject_css(html: str, css_text: str) -> str:
    style_tag = f"\n<style>\n{css_text}\n</style>\n"
    if "</head>" in html:
        return html.replace("</head>", style_tag + "</head>", 1)
    return style_tag + html
