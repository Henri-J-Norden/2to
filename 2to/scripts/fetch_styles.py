from __future__ import annotations

import argparse
import asyncio
import logging
import re
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import aiohttp


# Download a wide selection of CSS styles into from2to/styles/included/
STYLES: dict[str, List[Tuple[str, str]]] = {
    # Minimalist site styles
    "https://cdn.jsdelivr.net/npm/water.css@latest/LICENSE.md": [
        ("water", "https://cdn.jsdelivr.net/npm/water.css@latest/out/water.min.css"),
        ("water-dark", "https://cdn.jsdelivr.net/npm/water.css@latest/out/dark.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/sakura.css@latest/LICENSE.txt": [
        ("sakura", "https://cdn.jsdelivr.net/npm/sakura.css@latest/css/sakura.min.css"),
        ("sakura-dark", "https://cdn.jsdelivr.net/npm/sakura.css@latest/css/sakura-dark.min.css"),
    ],
    "https://unpkg.com/mvp.css@1.17.2/LICENSE": [
        ("mvp", "https://unpkg.com/mvp.css@latest/mvp.css"),
    ],
    "https://cdn.jsdelivr.net/npm/@exampledev/new.css@latest/LICENSE": [
        ("new", "https://cdn.jsdelivr.net/npm/@exampledev/new.css@latest/new.min.css"),
    ],
    "https://cdn.jsdelivr.net/gh/kevquirk/simple.css@latest/LICENSE": [
        ("simple", "https://cdn.jsdelivr.net/gh/kevquirk/simple.css@latest/simple.min.css"),
    ],
    "https://unpkg.com/@picocss/pico@latest/LICENSE.md": [
        ("pico", "https://unpkg.com/@picocss/pico@latest/css/pico.min.css"),
    ],
    "https://unpkg.com/awsm.css@latest/LICENSE": [
        ("awsm", "https://unpkg.com/awsm.css@latest/dist/awsm.min.css"),
    ],
    "https://unpkg.com/marx-css@latest/LICENSE.md": [
        ("marx", "https://unpkg.com/marx-css@latest/css/marx.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/milligram@latest/license": [
        ("milligram", "https://cdn.jsdelivr.net/npm/milligram@latest/dist/milligram.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/skeleton-css@latest/LICENSE.md": [
        ("skeleton", "https://cdn.jsdelivr.net/npm/skeleton-css@latest/css/skeleton.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/bulma@latest/LICENSE": [
        ("bulma", "https://cdn.jsdelivr.net/npm/bulma@latest/css/bulma.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/bootstrap@latest/LICENSE": [
        ("bootstrap", "https://cdn.jsdelivr.net/npm/bootstrap@latest/dist/css/bootstrap.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/bootswatch@latest/LICENSE": [
        ("bootswatch-darkly", "https://cdn.jsdelivr.net/npm/bootswatch@latest/dist/darkly/bootstrap.min.css"),
    ],
    "https://unpkg.com/chota@latest/LICENSE": [
        ("chota", "https://unpkg.com/chota@latest/dist/chota.min.css"),
    ],
    "https://unpkg.com/picnic@latest/LICENSE": [
        ("picnic", "https://unpkg.com/picnic@latest/picnic.min.css"),
    ],
    "https://unpkg.com/purecss@latest/LICENSE": [
        ("pure", "https://unpkg.com/purecss@latest/build/pure-min.css"),
    ],
    "https://unpkg.com/tachyons@latest/LICENSE": [
        ("tachyons", "https://unpkg.com/tachyons@latest/css/tachyons.min.css"),
    ],
    "https://unpkg.com/spectre.css@latest/LICENSE": [
        ("spectre", "https://unpkg.com/spectre.css@latest/dist/spectre.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/mini.css@latest/LICENSE": [
        ("mini", "https://cdn.jsdelivr.net/npm/mini.css@latest/dist/mini-default.min.css"),
    ],
    "https://unpkg.com/wingcss@latest/LICENSE": [
        ("wing", "https://unpkg.com/wingcss@latest/dist/wing.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/sanitize.css@latest/LICENSE.md": [
        ("sanitize", "https://cdn.jsdelivr.net/npm/sanitize.css@latest/sanitize.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/siimple@latest/LICENSE": [
        ("siimple", "https://cdn.jsdelivr.net/npm/siimple@latest/siimple.min.css"),
    ],
    "https://unpkg.com/turretcss@latest/LICENSE": [
        ("turret", "https://unpkg.com/turretcss@latest/dist/turretcss.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/paper-css@latest/LICENSE": [
        ("paper", "https://cdn.jsdelivr.net/npm/paper-css@latest/paper.min.css"),
    ],
    "https://latex.vercel.app/LICENSE": [
        ("latex", "https://latex.vercel.app/style.css"),
    ],
    "https://cdn.jsdelivr.net/npm/tufte-css@latest/LICENSE": [
        ("tufte", "https://cdn.jsdelivr.net/npm/tufte-css@latest/tufte.min.css"),
    ],
    "https://cdn.jsdelivr.net/npm/github-markdown-css@latest/license": [
        ("github", "https://cdn.jsdelivr.net/npm/github-markdown-css@latest/github-markdown-light.min.css"),
        ("github-dark", "https://cdn.jsdelivr.net/npm/github-markdown-css@latest/github-markdown-dark.min.css"),
    ],
}


def get_styles_dir() -> Path:
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent
    styles_dir = root_dir / "from2to" / "styles" / "included"
    return styles_dir


async def fetch_one(
    session: aiohttp.ClientSession,
    name: str,
    url: str,
    out_dir: Path,
    *,
    retries: int,
    retry_delay: float,
    timeout_seconds: float,
) -> bool:
    dest = out_dir / f"{name}.css"
    attempt = 0
    while attempt < retries:
        attempt += 1
        try:
            async with session.get(url, timeout=timeout_seconds) as resp:
                resp.raise_for_status()
                data = await resp.read()
            dest.write_bytes(data)
            logging.info("Downloaded %s -> %s", name, dest)
            return True
        except Exception as exc:
            logging.warning("Attempt %s/%s failed for %s: %s", attempt, retries, name, exc)
            if attempt < retries:
                await asyncio.sleep(retry_delay)
    logging.error("Failed to download %s after %s attempts", name, retries)
    return False


async def fetch_all(
    selected: Iterable[Tuple[str, str, str]],
    *,
    concurrency: int,
    retries: int,
    retry_delay: float,
    timeout_seconds: float,
) -> int:
    out_dir = get_styles_dir()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sem = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        async def runner(name: str, url: str) -> bool:
            async with sem:
                return await fetch_one(
                    session,
                    name,
                    url,
                    out_dir,
                    retries=retries,
                    retry_delay=retry_delay,
                    timeout_seconds=timeout_seconds,
                )

        tasks = [runner(name, url) for name, url, _license_url in selected]
        results = await asyncio.gather(*tasks)

    failures = len([r for r in results if not r])
    return failures


async def fetch_license_text(
    session: aiohttp.ClientSession,
    license_url: str,
    *,
    retries: int,
    retry_delay: float,
    timeout_seconds: float,
) -> str | None:
    attempt = 0
    while attempt < retries:
        attempt += 1
        try:
            async with session.get(license_url, timeout=timeout_seconds) as resp:
                resp.raise_for_status()
                text = await resp.text()
            logging.info("Downloaded license %s", license_url)
            return text
        except Exception as exc:
            logging.warning(
                "Attempt %s/%s failed for license %s: %s", attempt, retries, license_url, exc
            )
            if attempt < retries:
                await asyncio.sleep(retry_delay)
    logging.error("Failed to download license %s after %s attempts", license_url, retries)
    return None


def write_license_file(license_texts: Dict[str, str], license_styles: Dict[str, List[str]]) -> None:
    styles_dir = get_styles_dir()
    dest = styles_dir.parent / "LICENSE.md"
    parts: List[str] = []
    summary_rows: List[str] = []

    # Preserve insertion order from license_styles (matches STYLES definition order)
    for license_url, styles in license_styles.items():
        if license_url not in license_texts:
            continue
        heading_styles = ", ".join(styles)

        raw_text = license_texts[license_url].lstrip()
        first_line = next((ln.strip() for ln in raw_text.splitlines() if ln.strip()), "")
        license_name = re.sub(r"^#+\s*", "", first_line) if first_line else "Unknown"

        license_text = re.sub(r"(^\s*#)", r"\1#", raw_text.rstrip(), flags=re.MULTILINE)

        summary_rows.append(f"| {heading_styles} | {license_name} |")
        parts.append(f"# [{heading_styles}]({license_url})\n{license_text}\n")

    summary_table = "\n".join(["| Styles | License |", "| --- | --- |"] + summary_rows)
    content = "\n".join(["# Summary", "", summary_table, ""]) + "\n---\n\n" + "\n---\n\n".join(parts).rstrip("\n") + "\n"
    dest.write_text(content, encoding="utf-8")
    logging.info("Wrote %s", dest)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch bundled CSS styles asynchronously.")
    parser.add_argument(
        "styles",
        nargs="*",
        help="Optional style names to fetch (default: all)",
    )
    parser.add_argument("--concurrency", type=int, default=8, help="Number of concurrent downloads")
    parser.add_argument("--retries", type=int, default=1, help="Download attempts per file")
    parser.add_argument("--retry-delay", type=float, default=2.0, help="Seconds to wait between retries")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def build_style_index() -> Dict[str, Tuple[str, str]]:
    index: Dict[str, Tuple[str, str]] = {}
    for license_url, styles in STYLES.items():
        for name, css_url in styles:
            index[name] = (css_url, license_url)
    return index


def filter_styles(names: Iterable[str]) -> Tuple[Tuple[str, str, str], ...]:
    index = build_style_index()
    if not names:
        return tuple((name, css_url, license_url) for name, (css_url, license_url) in index.items())
    requested = set(names)
    missing = requested - set(index)
    if missing:
        raise SystemExit(f"Unknown style names: {', '.join(sorted(missing))}")
    return tuple((name, index[name][0], index[name][1]) for name in names)


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")
    selected = filter_styles(args.styles)
    logging.info("Downloading %s style(s) into %s", len(selected), get_styles_dir())
    style_failures = asyncio.run(
        fetch_all(
            selected,
            concurrency=args.concurrency,
            retries=args.retries,
            retry_delay=args.retry_delay,
            timeout_seconds=args.timeout,
        )
    )

    license_styles: Dict[str, List[str]] = {}
    for name, _css_url, license_url in selected:
        license_styles.setdefault(license_url, []).append(name)

    async def fetch_licenses() -> Dict[str, str]:
        async with aiohttp.ClientSession() as session:
            tasks = {
                license_url: fetch_license_text(
                    session,
                    license_url,
                    retries=args.retries,
                    retry_delay=args.retry_delay,
                    timeout_seconds=args.timeout,
                )
                for license_url in license_styles
            }
            results = await asyncio.gather(*tasks.values())
        return {lic: text for lic, text in zip(tasks.keys(), results) if text is not None}

    license_texts = asyncio.run(fetch_licenses())

    missing_licenses = set(license_styles) - set(license_texts)
    if missing_licenses:
        logging.error("Failed to download %s license(s)", len(missing_licenses))
    write_license_file(license_texts, license_styles)

    total_failures = style_failures + len(missing_licenses)
    if total_failures:
        logging.error("Completed with %s failure(s)", total_failures)
        return 1
    logging.info("Done. Downloaded styles into %s", get_styles_dir())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
