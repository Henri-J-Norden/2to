import argparse
import io
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Optional, Tuple, List
from urllib.parse import urlparse

import pypandoc  # provided by pypandoc-binary
from xhtml2pdf import pisa

PACKAGE_NAME = "md2pdf2"
DEFAULT_STYLE = "water"


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
        test_file.unlink(missing_ok=True)  # type: ignore[call-arg]
        return pkg_cache
    except Exception:
        pass

    # Fall back to user cache dirs
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

    # Helper to read file text
    def read_css(path: Path) -> str:
        return path.read_text(encoding="utf-8")

    # candidates not needed; we resolve directly via lookups below

    if is_url(style):
        # Derive filename from URL path
        url_path = urlparse(style).path
        name = Path(url_path).name or "style.css"
        if not name.endswith(".css"):
            name = f"{name}.css"
        if no_cache:
            tmp = Path(tempfile.gettempdir()) / f"md2pdf2-{name}"
            download_url(style, tmp)
            return (read_css(tmp), tmp)
        else:
            cdir.mkdir(parents=True, exist_ok=True)
            target = cdir / name
            if not target.exists():
                download_url(style, target)
            return (read_css(target), target)

    # Local path
    p = Path(style)
    if p.is_file():
        return (read_css(p), p.resolve())

    names = [style]
    if not style.endswith(".css"):
        names.append(f"{style}.css")

    # Cache dir lookup
    for nm in names:
        cp = cdir / nm
        if cp.is_file():
            return (read_css(cp), cp)

    # Included styles lookup
    inc_root = get_package_root() / "styles" / "included"
    for nm in names:
        ip = inc_root / nm
        if ip.is_file():
            return (read_css(ip), ip)

    raise FileNotFoundError(
        f"Could not resolve style '{style}'. Use URL, file path, cached name, or included name."
    )


def download_url(url: str, dest: Path) -> None:
    # Avoid adding requests dependency; use urllib
    import urllib.request

    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def inject_css(html: str, css_text: str) -> str:
    style_tag = f"\n<style>\n{css_text}\n</style>\n"
    # Insert before </head> if possible; else at top
    if "</head>" in html:
        return html.replace("</head>", style_tag + "</head>", 1)
    return style_tag + html


def convert_markdown_to_html(
    input_md: Path,
    pandoc_args: Optional[Iterable[str]] = None,
    title: Optional[str] = None,
    toc: bool = False,
) -> str:
    extra_args = ["--standalone", "--from=markdown", "--to=html"]
    if title:
        extra_args += [f"--metadata=title:{title}"]
    if toc:
        extra_args += ["--toc"]
    if pandoc_args:
        extra_args += list(pandoc_args)
    html = pypandoc.convert_file(str(input_md), to="html", extra_args=extra_args)
    return html


def link_callback(uri: str, rel: str) -> str:
    """Convert HTML URIs to absolute file paths for xhtml2pdf."""
    # If already absolute file path
    p = Path(uri)
    if p.exists():
        return str(p)

    # file:// URI
    if uri.startswith("file://"):
        return uri[7:]

    # Relative resource path to current working directory
    rp = Path(rel).parent / uri
    if rp.exists():
        return str(rp)

    # Last resort: return original
    return uri


def html_to_pdf_bytes(html: str, base_path: Path) -> bytes:
    # Ensure that relative resources resolve relative to base_path
    # xhtml2pdf uses pisa.CreatePDF; provide link_callback for images/fonts
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(  # type: ignore
        src=html,
        dest=result,
        link_callback=lambda uri, rel: link_callback(uri, str(base_path)),
        encoding="utf-8",
    )
    if pisa_status.err:
        raise RuntimeError("PDF generation failed")
    return result.getvalue()


def compute_output_path(input_md: Path, output: Optional[str]) -> Path:
    if output:
        return Path(output)
    return input_md.with_suffix(".pdf")


def list_styles_command(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    print("Included styles:")
    for name in list_included_styles():
        print(f"  {name}")
    print("\nCached styles:")
    for name in list_cached_styles(cache_dir):
        print(f"  {name}")
    return 0


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="md2pdf2",
        description="Convert Markdown to PDF using bundled pandoc and xhtml2pdf, with CSS style management.",
    )
    p.add_argument("input", help="Path to input Markdown file")
    p.add_argument("-s", "--style", default=DEFAULT_STYLE, help="CSS style name, path, or URL (default: water)")
    p.add_argument("--no-cache", action="store_true", help="Do not cache downloaded URL styles; use a temp file")
    p.add_argument("--list-styles", action="store_true", help="List available included and cached styles and exit")
    p.add_argument("-o", "--output", help="Output PDF path (default: same as input with .pdf)")
    p.add_argument("--stdout", action="store_true", help="Write PDF to stdout instead of a file")
    p.add_argument("--title", help="Set document title")
    p.add_argument("--toc", action="store_true", help="Enable table of contents via pandoc")
    p.add_argument(
        "--pandoc-arg",
        action="append",
        nargs="+",
        default=[],
        help="Extra pandoc arg(s) (repeatable)",
    )
    p.add_argument("--cache-dir", help="Override cache directory")
    return p.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)

    if args.list_styles:
        return list_styles_command(args)

    input_md = Path(args.input)
    if not input_md.is_file():
        print(f"Input file not found: {input_md}", file=sys.stderr)
        return 2

    cache_dir = Path(args.cache_dir) if args.cache_dir else None

    try:
        css_text, css_path = resolve_style(args.style, cache_dir=cache_dir, no_cache=args.no_cache)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    # Flatten pandoc args in case argparse aggregated them (support both list and list-of-lists)
    pandoc_extra: List[str] = []
    for item in (args.pandoc_arg or []):
        if isinstance(item, (list, tuple)):
            pandoc_extra.extend(item)
        else:
            pandoc_extra.append(item)

    # Convert MD -> HTML
    html = convert_markdown_to_html(
        input_md,
        pandoc_args=pandoc_extra,
        title=args.title or input_md.stem,
        toc=args.toc,
    )

    # Inject CSS inline
    html = inject_css(html, css_text)

    # Produce PDF bytes
    try:
        pdf_bytes = html_to_pdf_bytes(html, base_path=input_md.resolve())
    except Exception as e:
        print(f"Error during PDF generation: {e}", file=sys.stderr)
        return 1

    if args.stdout:
        sys.stdout.buffer.write(pdf_bytes)
        return 0

    out_path = compute_output_path(input_md, args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(pdf_bytes)
    print(f"Wrote: {out_path}")
    return 0


def clear_cache(cache_dir: Optional[Path] = None) -> int:
    cdir = cache_dir or get_default_cache_dir()
    if not cdir.exists():
        print("Cache directory does not exist; nothing to clear.")
        return 0
    removed = 0
    for p in cdir.glob("*.css"):
        try:
            p.unlink()
            removed += 1
        except Exception:
            pass
    print(f"Removed {removed} cached files from {cdir}")
    return 0


def clear_cache_main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="md2pdf2-clear-cache", description="Clear the md2pdf2 style download cache")
    p.add_argument("--cache-dir", help="Override cache directory")
    args = p.parse_args(list(argv) if argv is not None else None)
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    return clear_cache(cache_dir)


if __name__ == "__main__":
    raise SystemExit(main())
