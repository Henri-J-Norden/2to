from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pypandoc  # provided by pypandoc-binary


def convert_markdown_to_html(
    input_md: Path,
    pandoc_args: Optional[Iterable[str]] = None,
    title: Optional[str] = None,
    toc: bool = False,
) -> str:
    extra_args = ["--standalone", "--from=markdown", "--to=html"]
    if title:
        extra_args += [f"--metadata=title:{title}"]
    if toc:
        extra_args += ["--toc"]
    if pandoc_args:
        # flatten in case list-of-lists
        for item in pandoc_args:
            if isinstance(item, (list, tuple)):
                extra_args.extend(item)
            else:
                extra_args.append(item)
    html = pypandoc.convert_file(str(input_md), to="html", extra_args=extra_args)
    return html


def convert_markdown_to_pdf(
    input_md: Path,
    pandoc_args: Optional[Iterable[str]] = None,
    title: Optional[str] = None,
    toc: bool = False,
    **kwargs,
) -> str:
    extra_args = ["--standalone", "--from=markdown"]
    if title:
        extra_args += [f"--metadata=title:{title}"]
    if toc:
        extra_args += ["--toc"]
    if pandoc_args:
        # flatten in case list-of-lists
        for item in pandoc_args:
            if isinstance(item, (list, tuple)):
                extra_args.extend(item)
            else:
                extra_args.append(item)
    print(kwargs.get("outputfile"))
    html = pypandoc.convert_file(str(input_md), to="pdf", extra_args=extra_args, **kwargs)
    return html
