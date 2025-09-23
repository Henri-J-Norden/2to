#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

# Download a wide selection of CSS styles into pdf2md2/styles/included/
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Join-Path $ScriptDir '..'
$OutDir = Join-Path $RootDir 'pdf2md2/styles/included'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Use-Curl {
    param (
        [string]$Url,
        [string]$OutFile
    )
    $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
    if ($null -ne $curl) {
        & $curl.Path '-fsSL' '--retry' '3' '--retry-delay' '2' '-o' $OutFile $Url
    } else {
        # Fallback to Invoke-WebRequest (PowerShell's web client)
        Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
    }
}

function Fetch {
    param (
        [string]$Name,
        [string]$Url
    )
    $out = Join-Path $OutDir "$Name.css"
    Write-Host "Downloading $Name -> $out"
    Use-Curl -Url $Url -OutFile $out
}

# Minimalist site styles
Fetch 'water' 'https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'
Fetch 'water-dark' 'https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css'
Fetch 'sakura' 'https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css'
Fetch 'sakura-dark' 'https://cdn.jsdelivr.net/npm/sakura.css/css/sakura-dark.css'
Fetch 'mvp' 'https://unpkg.com/mvp.css'
Fetch 'new' 'https://newcss.net/new.min.css'
Fetch 'simple' 'https://cdn.jsdelivr.net/gh/kevquirk/simple.css@1.2.0/simple.min.css'
Fetch 'pico' 'https://unpkg.com/@picocss/pico@1/css/pico.min.css'
Fetch 'awsm' 'https://unpkg.com/awsm.css/dist/awsm.min.css'
Fetch 'marx' 'https://unpkg.com/marx-css/css/marx.min.css'
Fetch 'milligram' 'https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.min.css'
Fetch 'skeleton' 'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css'
Fetch 'bulma' 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css'
Fetch 'bootstrap' 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'
Fetch 'chota' 'https://unpkg.com/chota@latest/dist/chota.min.css'
Fetch 'picnic' 'https://unpkg.com/picnic@7.1.0/picnic.min.css'
Fetch 'pure' 'https://unpkg.com/purecss@3.0.0/build/pure-min.css'
Fetch 'tachyons' 'https://unpkg.com/tachyons@4.12.0/css/tachyons.min.css'
Fetch 'spectre' 'https://unpkg.com/spectre.css/dist/spectre.min.css'
Fetch 'wing' 'https://unpkg.com/wingcss@0.1.8/dist/wing.min.css'
Fetch 'sanitize' 'https://unpkg.com/sanitize.css@13.0.0/sanitize.css'
Fetch 'siimple' 'https://unpkg.com/siimple@3.3.1/dist/siimple.min.css'
Fetch 'turretcss' 'https://unpkg.com/turretcss@6.1.3/dist/turretcss.min.css'
Fetch 'papercss' 'https://unpkg.com/papercss@1.9.2/dist/paper.min.css'
Fetch 'latex' 'https://cdn.jsdelivr.net/gh/vincentdoerig/latex-css@v1.7.6/css/latex.min.css'
Fetch 'tufte' 'https://cdn.jsdelivr.net/gh/edwardtufte/tufte-css/tufte.css'
Fetch 'github-markdown' 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.7.0/github-markdown.min.css'

# Code highlighting themes (optional)
Fetch 'highlightjs-default' 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css'
Fetch 'highlightjs-github' 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css'
Fetch 'highlightjs-monokai-sublime' 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/monokai-sublime.min.css'
Fetch 'highlightjs-solarized-dark' 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/solarized-dark.min.css'
Fetch 'highlightjs-solarized-light' 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/solarized-light.min.css'
Fetch 'prism-default' 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css'
Fetch 'prism-okaidia' 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css'
Fetch 'prism-tomorrow' 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css'

Write-Host "Done. Downloaded styles into $OutDir" -ForegroundColor Green
