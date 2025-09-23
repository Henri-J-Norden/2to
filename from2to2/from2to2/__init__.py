"""from2to2 common package

Shared utilities for style management, caching, and common CLI helpers.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("from2to2")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["__version__"]
