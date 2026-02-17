# 2pdf

Easy Markdown → PDF conversion, with nice looking defaults, custom style support and zero external dependencies (everything is bundled):

```bash
uvx 2pdf README.md
```

_Result is written to README.pdf_

---

## Additional options
For more options, run:

```bash
uvx 2pdf --help
```

- `-s, --style STYLE` — Style name, local path, or URL. Default: `water`.
  - There are many bundled stylesheets: `water`, `sakura`, `github`, `latex`, `tufte`, etc.
  - `--list-styles` — List included and cached styles.
  -
- `-o, --output PATH` — Output PDF path (defaults to input with `.pdf`).
- `--stdout` — Write PDF to stdout instead of a file.

- `--no-cache` — For URL styles, download to a temp file instead of caching.
- `--title`, `--toc`, `--pandoc-arg …` — Pass through to Pandoc. See `--help`.

Use `2pdf-clear-cache` to clear the style download cache.

## Styles

The package includes a large set of popular CSS styles (e.g., water.css, sakura.css, GitHub Markdown CSS, latex.css, Tufte.css, etc.).

You can also point to any CSS URL:

```bash
2pdf notes.md -s https://cdn.jsdelivr.net/npm/water.css@2/out/water.css
```

Or use a local file:

```bash
2pdf notes.md -s /path/to/custom.css
```

To see available styles:

```bash
2pdf --list-styles
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
