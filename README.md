# pdf2md2

Markdown to PDF CLI using bundled Pandoc (via pypandoc-binary) and a built-in CSS style system with caching.

- Uses `pypandoc-binary` so no external pandoc install is needed.
- Converts Markdown → HTML (Pandoc) → PDF (xhtml2pdf) to avoid external PDF engines.
- Supports many CSS stylesheets (included in the package), plus style download caching.
- Provides two CLI commands: `pdf2md2` and `pdf2md2-clear-cache`.

## Install and Run using uv

```bash
uv pip install pdf2md2
uvx pdf2md2 README.md -s water
```

Or run directly with Python:

```bash
python -m pdf2md2 README.md -s github -o output.pdf
```

## CLI

```bash
pdf2md2 [-h] [-s STYLE] [--no-cache] [--list-styles] [-o OUTPUT] [--stdout]
        [--title TITLE] [--toc] [--pandoc-arg ARG ...] [--cache-dir PATH]
        INPUT
```

- `INPUT`: path to a Markdown file.
- `-s, --style STYLE`: CSS style to use. Default: `water`.
  - If URL, the CSS is downloaded to the package cache (unless `--no-cache`), then used.
  - If a valid file path, that CSS file is used.
  - Else, looks for a cached file in the package cache (`{STYLE}` or `{STYLE}.css`).
  - Else, looks for a built-in included style in the package (`{STYLE}` or `{STYLE}.css`).
- `--no-cache`: for URL styles only, download to a temp file instead of caching.
- `--list-styles`: list available included and cached styles.
- `-o, --output`: output PDF path. Defaults to the same directory/name as input, with `.pdf` extension.
- `--stdout`: write PDF to stdout instead of a file.
- `--title`: set the HTML/PDF document title (defaults to the input filename).
- `--toc`: enable table of contents generation by pandoc.
- `--pandoc-arg`: additional arguments passed to pandoc (repeatable).
- `--cache-dir`: override the cache directory (by default we try the package install dir, fall back to `~/.cache/pdf2md2`).

```bash
pdf2md2-clear-cache [-h] [--cache-dir PATH]
```

Clears the download cache directory (for URL styles).

## Styles

The package includes a large set of popular CSS styles (e.g., water.css, sakura.css, GitHub Markdown CSS, latex.css, Tufte.css, etc.).

You can also point to any CSS URL:

```bash
pdf2md2 notes.md -s https://cdn.jsdelivr.net/npm/water.css@2/out/water.css
```

Or use a local file:

```bash
pdf2md2 notes.md -s /path/to/custom.css
```

To see available styles:

```bash
pdf2md2 --list-styles
```

## Notes

- xhtml2pdf supports a subset of CSS 2.1. Some advanced CSS may not render exactly as in a web browser.
- Images and local assets referenced in the Markdown are resolved relative to the input file directory.
- If the package install directory isn't writeable for caching URL styles, we fallback to `~/.cache/pdf2md2` unless `--cache-dir` is supplied.

## License

MIT
