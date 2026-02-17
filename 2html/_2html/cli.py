import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

from rich_argparse import RichHelpFormatter

from from2to import style_utils as su
from from2to import convert as conv
from from2to import cli_common as cc


def compute_output_path(input_md: Path, output: Optional[str]) -> Path:
    if output:
        return Path(output)
    return input_md.with_suffix(".html")


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="2html",
        description="Convert Markdown to HTML using bundled pandoc, with CSS style management.",
        formatter_class=RichHelpFormatter,
    )
    p.add_argument("input", help="Path to input Markdown file")
    p.add_argument("-o", "--output", help="Output HTML path (default: input, but with .html extension)")
    p.add_argument("-b", "--browse", action="store_true", help="Open the HTML file in a browser after conversion")
    cc.add_common_args(p)
    args = p.parse_args(argv)
    args = cc.post_parse_args(args)
    return args


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)

    if args.list_styles:
        return cc.list_styles_command(args)

    input_md = Path(args.input)
    if not input_md.is_file():
        print(f"Input file not found: {input_md}", file=sys.stderr)
        return 2

    cache_dir = Path(args.cache_dir) if args.cache_dir else None

    try:
        css_text, css_path = su.resolve_style(args.style, cache_dir=cache_dir, no_cache=args.no_cache)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    # Convert MD -> HTML
    html = conv.convert_markdown_to_html(
        input_md,
        pandoc_args=args.pandoc_arg,
        title=args.title or input_md.stem,
        toc=args.toc,
    )

    # Inject CSS inline
    html = su.inject_css(html, css_text)

    if args.stdout:
        sys.stdout.write(html)
        return 0

    out_path = compute_output_path(input_md, args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote: {out_path}")

    if args.browse:
        import webbrowser
        webbrowser.open(out_path.absolute().as_uri())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
