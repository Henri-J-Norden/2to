Write the Python package pdf2md2, using uv and setuptools, that:
- provides a CLI script pdf2md2 (so it's usable with uvx)
- uses pandoc via pypandoc_binary (so there are no external dependencies - requirement for uvx)
- has a CLI arg for the style "-s"/"--style", "water" by default
  - includes a bunch of common CSS stylesheets in the package by default (decide upon a wide selection - like really way too many to be reasonable - and use curl to download them to a separate dir)
- the style arg should work as follows:
  - if it's an URL, download the style to a cache dir in the package install dir and use that
  - elif it's a valid path, use the local file
  - elif it's a file in the package download cache (as "{style}" or "{style}.css"), use that
  - elif it's a file in the package included styles (as "{style}" or "{style}.css"), use that
- has a CLI arg "--no-cache"
- has other appropriate CLI args
- takes a (markdown) file as a positional argument
- outputs a PDF file in the same directory by default, with the same name (only changed extension)
- has a CLI arg "-o"/"--output" to override the output path
- has a CLI arg "--stdout" to write to stdout instead of a file
- provides a script `pdf2md2-clear-cache` to clear the download cache


Remove the powershell script (assume everyone has bash and curl)


Fuck, I fucked up the package name and you just used it everywhere... it should be md2pdf2 not pdf2md2! Fix it

Also simplify the README:
- README should start with a single sentence description and usage with uvx. More in-depth description and usage should come later (remember this)
- Do not list the entire fucking CLI help in the readme (tell them to use --help) - only the more important options
- Add a development section:
  - editable install locally in a .venv using uv
  - run the style update script


Split the md2pdf2 package into a common from2to package and a md2pdf2 package and md2html2 packages that use it. Avoid code duplication and remember that there will be more derived conversion packages in the future.

Obvious things that should be in the common package:
- common CLI arg parsing
- included styles
- style download cache
- style management commands
- etc

Implement these as package directories within the project root dir, each with their own pyproject.toml. The root dir should have a pyproject.toml that defines a uv workspace and includes all the packages.


Continue.

I can see there is a lot of useless boilerplate:
```
def clear_cache(cache_dir: Optional[Path] = None) -> int:
    return cc.clear_cache(cache_dir)


def clear_cache_main(argv: Optional[Iterable[str]] = None) -> int:
    return cc.clear_cache_main(argv)

def inject_css(html: str, css_text: str) -> str:
    return su.inject_css(html, css_text)
```
Just import the functions and use them directly...

Also make sure the main() of each package is *actually* minimal and avoids code duplication as much as reasonable (with shared common code in from2to).
