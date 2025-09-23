# md2pdf2

Minimal, zero-external-deps Markdown → PDF using bundled Pandoc (pypandoc-binary), CSS styles, and caching.

Quick usage with uvx:

```bash
uvx md2pdf2 README.md -s water
```

For more options, run:

```bash
uvx md2pdf2 --help
```

## Key options

- `-s, --style STYLE` — Style name, local path, or URL. Default: `water`.
- `-o, --output PATH` — Output PDF path (defaults to input with `.pdf`).
- `--stdout` — Write PDF to stdout instead of a file.
- `--list-styles` — List included and cached styles.
- `--no-cache` — For URL styles, download to a temp file instead of caching.
- `--title`, `--toc`, `--pandoc-arg …` — Pass through to Pandoc. See `--help`.

Use `md2pdf2-clear-cache` to clear the style download cache.

## Styles

The package includes a large set of popular CSS styles (e.g., water.css, sakura.css, GitHub Markdown CSS, latex.css, Tufte.css, etc.).

You can also point to any CSS URL:

```bash
md2pdf2 notes.md -s https://cdn.jsdelivr.net/npm/water.css@2/out/water.css
```

Or use a local file:

```bash
md2pdf2 notes.md -s /path/to/custom.css
```

To see available styles:

```bash
md2pdf2 --list-styles
```

## Notes

- xhtml2pdf supports a subset of CSS 2.1. Some advanced CSS may not render exactly as in a web browser.
- Images and local assets referenced in the Markdown are resolved relative to the input file directory.
- If the package install directory isn't writeable for caching URL styles, we fallback to a user cache dir unless `--cache-dir` is supplied.

## Development

Use uv for an isolated local environment and editable install.

```bash
uv venv --seed
uv pip install -e .

# Populate or refresh included styles (requires bash + curl)
bash scripts/fetch_styles.sh
```

## License

MIT
