import argparse
import os
from pathlib import Path
from typing import Iterable, Optional

from . import style_utils as su


def add_common_args(p: argparse.ArgumentParser) -> argparse.ArgumentParser:
    p.add_argument("--stdout", action="store_true", help="Write to stdout instead of a file")

    style_group = p.add_argument_group("Style options")
    style_group.add_argument("-s", "--style", default=None, help=f"CSS style name, path, or URL (default: {su.DEFAULT_STYLE}) \[env: FROM2TO_STYLE={os.environ.get('FROM2TO_STYLE', '')}]")
    style_group.add_argument("--list-styles", action="store_true", help="List available included and cached styles and exit")
    style_group.add_argument("--no-cache", action="store_true", help="Do not cache downloaded URL styles; use a temp file")
    style_group.add_argument("--cache-dir", help="Override cache directory")

    content_group = p.add_argument_group("Content options")
    content_group.add_argument("--title", help="Set document title")
    content_group.add_argument("--toc", action="store_true", help="Enable table of contents via pandoc")
    content_group.add_argument(
        "--pandoc-arg",
        action="append",
        nargs="+",
        default=[],
        help="Extra pandoc arg(s) (repeatable)",
    )
    return p


def post_parse_args(args: argparse.Namespace) -> argparse.Namespace:
    if args.style is None:
        if "FROM2TO_STYLE" in os.environ:
            args.style = os.environ["FROM2TO_STYLE"]
        else:
            args.style = su.DEFAULT_STYLE
    return args


def list_styles_command(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    print("Included styles:")
    for name in su.list_included_styles():
        print(f"  {name}")
    print("\nCached styles:")
    for name in su.list_cached_styles(cache_dir):
        print(f"  {name}")
    return 0


def clear_cache(cache_dir: Optional[Path] = None) -> int:
    cdir = cache_dir or su.get_default_cache_dir()
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
    p = argparse.ArgumentParser(prog="from2to-clear-cache", description="Clear the common style download cache")
    p.add_argument("--cache-dir", help="Override cache directory")
    args = p.parse_args(list(argv) if argv is not None else None)
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    return clear_cache(cache_dir)
