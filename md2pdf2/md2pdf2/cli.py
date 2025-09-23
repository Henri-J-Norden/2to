import argparse
import io
import sys
from pathlib import Path
from typing import Iterable, Optional

from xhtml2pdf import pisa

from from2to2 import style_utils as su
from from2to2 import convert as conv
from from2to2 import cli_common as cc


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


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="md2pdf2",
        description="Convert Markdown to PDF using bundled pandoc and xhtml2pdf, with CSS style management.",
    )
    p.add_argument("input", help="Path to input Markdown file")
    p.add_argument("-o", "--output", help="Output PDF path (default: same as input with .pdf)")
    cc.add_common_args(p)
    return p.parse_args(argv)


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


if __name__ == "__main__":
    raise SystemExit(main())
