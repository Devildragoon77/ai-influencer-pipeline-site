#!/usr/bin/env python3
"""Build guide HTML pages from the GUIDES dict below, plus guides/index.html
and sitemap.xml. Keeps every page on the same styling as the landing page.

usage: python _template.py <base_url>
"""
import html
import os
import sys

STYLE = """
  :root { --bg:#0a0a0c; --panel:#141418; --text:#e8e8ec; --dim:#9a9aa4; --accent:#ff90e8; --line:#26262c; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font:17px/1.7 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .wrap { max-width:760px; margin:0 auto; padding:40px 20px 80px; }
  a { color:var(--accent); }
  h1 { font-size:2rem; line-height:1.25; margin:18px 0 6px; letter-spacing:-.4px; }
  h2 { font-size:1.35rem; margin:34px 0 10px; }
  h3 { font-size:1.1rem; margin:24px 0 8px; }
  p, li { color:#c9c9d2; margin-bottom:14px; }
  ul, ol { margin:0 0 14px 22px; }
  li { margin-bottom:6px; }
  code { background:var(--panel); border:1px solid var(--line); border-radius:4px; padding:1px 6px; font-size:.9em; }
  pre { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; overflow-x:auto; margin-bottom:14px; }
  pre code { border:0; padding:0; }
  .crumb { color:var(--dim); font-size:.85rem; }
  .crumb a { color:var(--dim); }
  .meta { color:var(--dim); font-size:.9rem; margin-bottom:24px; }
  .cta { background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--accent); border-radius:0 10px 10px 0; padding:18px 20px; margin:30px 0; }
  .cta a { font-weight:700; }
  table { border-collapse:collapse; width:100%; margin-bottom:14px; font-size:.92rem; }
  th, td { border:1px solid var(--line); padding:8px 10px; text-align:left; color:#c9c9d2; }
  th { background:var(--panel); }
  footer { border-top:1px solid var(--line); margin-top:50px; padding-top:20px; color:var(--dim); font-size:.85rem; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{style}</style>
</head>
<body>
<div class="wrap">
<p class="crumb"><a href="../index.html">AI Influencer Pipeline</a> / <a href="index.html">Guides</a></p>
<h1>{h1}</h1>
<p class="meta">Updated June 2026 · Written from a live production system, not theory.</p>
{body}
<div class="cta">{cta}</div>
<footer>All guides are based on the stack behind a real automated Instagram persona.
Get the full working system: <a href="https://lionheart886.gumroad.com/l/ai-influencer-pipeline-kit">AI Influencer Pipeline Kit</a>
· <a href="https://lionheart886.gumroad.com/l/reel-dna-extractor">Reel DNA Extractor</a></footer>
</div>
</body>
</html>"""


def build(guides, base_url):
    here = os.path.dirname(os.path.abspath(__file__))
    links = []
    for slug, g in guides.items():
        page = PAGE.format(title=html.escape(g["title"]), desc=html.escape(g["desc"]),
                           h1=html.escape(g["h1"]), body=g["body"], cta=g["cta"],
                           style=STYLE)
        with open(os.path.join(here, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        links.append(f'<li><a href="{slug}.html">{html.escape(g["h1"])}</a><br>'
                     f'<span style="color:var(--dim);font-size:.9rem">{html.escape(g["desc"])}</span></li>')
        print("built", slug)

    index_body = ("<ul style='list-style:none;margin-left:0'>" +
                  "".join(f"<div style='margin-bottom:18px'>{l}</div>" for l in links) + "</ul>")
    idx = PAGE.format(title="Guides — AI Influencer Automation",
                      desc="Practical guides on automating an AI influencer: n8n, Instagram Graph API, Kling, quality control, monetization.",
                      h1="Guides", body=index_body,
                      cta='New here? Start with <a href="how-to-create-an-ai-influencer.html">How to Create an AI Influencer in 2026</a>.',
                      style=STYLE)
    with open(os.path.join(here, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)

    urls = [f"{base_url}/", f"{base_url}/guides/index.html"] + \
           [f"{base_url}/guides/{s}.html" for s in guides]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    with open(os.path.join(here, "..", "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)
    print("built guides/index.html and sitemap.xml")


if __name__ == "__main__":
    from guides_content import GUIDES
    build(GUIDES, sys.argv[1] if len(sys.argv) > 1 else "https://example.github.io/site")
