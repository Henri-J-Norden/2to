"""pdf2md2 package

Markdown to PDF CLI using Pandoc (bundled via pypandoc-binary) and xhtml2pdf,
with CSS style management and download caching.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pdf2md2")
except PackageNotFoundError:  # pragma: no cover - during local dev without install
    __version__ = "0.0.0"

__all__ = ["__version__"]
