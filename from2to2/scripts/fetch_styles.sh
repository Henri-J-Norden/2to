#!/usr/bin/env bash
set -euo pipefail

# Download a wide selection of CSS styles into from2to2/styles/included/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
OUT_DIR="${ROOT_DIR}/from2to2/styles/included"
mkdir -p "${OUT_DIR}"

fetch() {
  local name="$1"; shift
  local url="$1"; shift
  local out="${OUT_DIR}/${name}.css"
  echo "Downloading ${name} -> ${out}"
  curl -fsSL --retry 3 --retry-delay 2 -o "${out}" "${url}" || (echo "Failed to download ${name}")
}

# Minimalist site styles
fetch water "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"
fetch water-dark "https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css"
fetch sakura "https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css"
fetch sakura-dark "https://cdn.jsdelivr.net/npm/sakura.css/css/sakura-dark.css"
fetch mvp "https://unpkg.com/mvp.css"
fetch new "https://newcss.net/new.min.css"
fetch simple "https://cdn.jsdelivr.net/gh/kevquirk/simple.css/simple.min.css"
fetch pico "https://unpkg.com/@picocss/pico@1/css/pico.min.css"
fetch awsm "https://unpkg.com/awsm.css/dist/awsm.min.css"
fetch marx "https://unpkg.com/marx-css/css/marx.min.css"
fetch milligram "https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.min.css"
fetch skeleton "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"
fetch bulma "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css"
fetch bootstrap "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
fetch bootswatch-darkly "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/darkly/bootstrap.min.css"
fetch chota "https://unpkg.com/chota@latest/dist/chota.min.css"
fetch picnic "https://unpkg.com/picnic@7.1.0/picnic.min.css"
fetch pure "https://unpkg.com/purecss@3.0.0/build/pure-min.css"
fetch tachyons "https://unpkg.com/tachyons@4.12.0/css/tachyons.min.css"
fetch spectre "https://unpkg.com/spectre.css/dist/spectre.min.css"
fetch mini "https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css"
fetch wing "https://unpkg.com/wingcss@0.1.8/dist/wing.min.css"
fetch sanitize "https://unpkg.com/sanitize.css@13.0.0/sanitize.css"
fetch siimple "https://unpkg.com/siimple@3.3.1/dist/siimple.min.css"
fetch turretcss "https://unpkg.com/turretcss/dist/turretcss.min.css"
fetch papercss "https://unpkg.com/papercss@1.9.2/dist/paper.min.css"
fetch latex "https://latex.vercel.app/style.css"
fetch tufte "https://cdn.jsdelivr.net/gh/edwardtufte/tufte-css/tufte.css"
fetch github-markdown "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.7.0/github-markdown.min.css"

# Code highlighting themes
#fetch highlightjs "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"
#fetch highlightjs-github "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css"
#fetch highlightjs-monokai-sublime "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/monokai-sublime.min.css"
#fetch prism-default "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css"
#fetch prism-okaidia "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css"
#fetch prism-tomorrow "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css"

echo "Done. Downloaded styles into ${OUT_DIR}"
