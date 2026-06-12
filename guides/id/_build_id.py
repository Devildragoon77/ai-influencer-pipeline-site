#!/usr/bin/env python3
"""Build the Bahasa Indonesia guide pages (guides/id/*.html + index)."""
import html
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _template import STYLE  # reuse styling
from guides_content_id import GUIDES

PAGE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{style}</style>
</head>
<body>
<div class="wrap">
<p class="crumb"><a href="../../index.html">AI Influencer Pipeline</a> / <a href="index.html">Panduan</a> · <a href="../index.html">English version</a></p>
<h1>{h1}</h1>
<p class="meta">Diperbarui Juni 2026 · Ditulis dari sistem produksi yang benar-benar jalan, bukan teori.</p>
{body}
<div class="cta">{cta}</div>
<footer>Semua panduan berdasarkan stack di balik persona Instagram otomatis yang nyata.
Sistem lengkapnya: <a href="https://lionheart886.gumroad.com/l/ai-influencer-pipeline-kit">AI Influencer Pipeline Kit</a>
· <a href="https://lionheart886.gumroad.com/l/reel-dna-extractor">Reel DNA Extractor</a></footer>
</div>
</body>
</html>"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    links = []
    for slug, g in GUIDES.items():
        page = PAGE.format(title=html.escape(g["title"]), desc=html.escape(g["desc"]),
                           h1=html.escape(g["h1"]), body=g["body"], cta=g["cta"], style=STYLE)
        with open(os.path.join(here, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        links.append(f'<div style="margin-bottom:18px"><li><a href="{slug}.html">{html.escape(g["h1"])}</a><br>'
                     f'<span style="color:var(--dim);font-size:.9rem">{html.escape(g["desc"])}</span></li></div>')
        print("built id/" + slug)

    idx = PAGE.format(
        title="Panduan Otomasi AI Influencer (Bahasa Indonesia)",
        desc="Panduan praktis otomasi AI influencer: n8n, Instagram Graph API, Kling motion control, quality control, dan monetisasi untuk pasar Indonesia.",
        h1="Panduan (Bahasa Indonesia)",
        body="<ul style='list-style:none;margin-left:0'>" + "".join(links) + "</ul>",
        cta='Baru mulai? Baca <a href="cara-membuat-ai-influencer.html">Cara Membuat AI Influencer di 2026</a> dulu.',
        style=STYLE)
    with open(os.path.join(here, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)
    print("built id/index.html")


if __name__ == "__main__":
    main()
