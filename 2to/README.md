# from2to

Common utilities shared by 2→2 converters (e.g., md2pdf2, md2html2):

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
