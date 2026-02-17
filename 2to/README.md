# from2to

Common utilities shared by markdown2x converters:
- [**2pdf**](../2pdf)
- [**2html**](../2html)


## Features
- Style resolution (URL, local, cache, included)
- Style download cache management
- Included CSS styles bundle
- Common CLI argument definitions
- Markdown→HTML conversion via bundled Pandoc (pypandoc-binary)

Used as a workspace dependency by downstream packages.


## Development
Run scripts with:
```bash
uv run scripts/fetch_styles.py
```
