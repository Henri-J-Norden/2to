"""md2html2 package

Markdown to HTML CLI using bundled Pandoc (pypandoc-binary) with CSS style management via from2to2.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("md2html2")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["__version__"]
