#!/usr/bin/env python3
"""
Nailed & Inspired — Blog Generator
-----------------------------------
Turns data/posts.json + data/products.json into:
  - blog.html                (the Journal index, auto-listing every post)
  - blog/<slug>.html         (one real, shareable page per post)

WHY THIS EXISTS
Hand-building an HTML file per post doesn't scale at 5-10 posts/day, and if a
product link lives inside dozens of separate files, changing that link means
editing every file. This script keeps content in two JSON files and generates
the actual pages from them, so:
  - Adding a post   = add one object to data/posts.json, re-run this script
  - Changing a product link = edit it once in data/products.json, re-run this
    script, and every post referencing that product updates automatically

HOW TO ADD POSTS (the daily workflow)
  1. Open data/posts.json
  2. Copy one post object, paste it at the top of the list, give it a new
     unique "slug" (lowercase, hyphens, no spaces — this becomes the URL)
  3. Fill in title / tag / date / excerpt / body / products
     - "body" is a list of blocks. Plain text = paragraph.
       "## Heading" = subheading. "> Quote" = pull-quote.
       Wrap *word* in single asterisks for emphasis.
     - "products" is a list of product IDs from data/products.json
  4. If you're linking a NEW digital product, add it once to
     data/products.json (id, name, price, url, note)
  5. Run:  python3 generate_site.py
  6. Upload/push the updated blog.html + blog/ folder to Vercel

BEFORE GOING LIVE
  Set DOMAIN below to your real domain so share links and social previews
  (Threads, Substack, iMessage, etc.) point to the right URL.
"""

import json
import os
import re
import html as html_lib

DOMAIN = "https://YOUR-DOMAIN.com"   # <-- set this once you know the live path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
BLOG_DIR = os.path.join(BASE_DIR, "blog")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(BLOG_DIR, exist_ok=True)


def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def read_template(name):
    with open(os.path.join(TEMPLATES_DIR, name), encoding="utf-8") as f:
        return f.read()


def render_inline(text):
    """*word* -> <em>word</em>, escape everything else safely-ish (content is trusted, own site)."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)


def render_body(blocks):
    out = []
    for block in blocks:
        block = block.strip()
        if block.startswith("## "):
            out.append(f"<h2>{render_inline(block[3:])}</h2>")
        elif block.startswith("> "):
            out.append(f"<blockquote>{render_inline(block[2:])}</blockquote>")
        else:
            out.append(f"<p>{render_inline(block)}</p>")
    return "\n    ".join(out)


def render_products(product_ids, products):
    if not product_ids:
        return ""
    cards = []
    for pid in product_ids:
        p = products.get(pid)
        if not p:
            print(f"  ! warning: product id '{pid}' not found in products.json — skipping")
            continue
        cards.append(f'''<a href="{p['url']}" class="product-card" target="_blank" rel="noopener">
        <div class="product-info">
          <span class="product-name">{p['name']}</span>
          <span class="product-note">{p['note']}</span>
        </div>
        <span class="product-price">{p['price']}</span>
      </a>''')
    if not cards:
        return ""
    return f'''
<section class="shop-section">
  <div class="wrap" style="max-width:720px;">
    <span class="kicker" style="color:var(--brick);">FOR HER NEXT STEP</span>
    <div class="product-grid">
      {"".join(cards)}
    </div>
  </div>
</section>
'''


def build_post_page(post, products, post_template, header_sub, footer_sub):
    body_html = render_body(post["body"])
    products_html = render_products(post.get("products", []), products)

    meta = f'''<meta name="description" content="{html_lib.escape(post['excerpt'])}">
<meta property="og:title" content="{html_lib.escape(post['title'])} — Nailed & Inspired">
<meta property="og:description" content="{html_lib.escape(post['excerpt'])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{DOMAIN}/blog/{post['slug']}.html">
<meta name="twitter:card" content="summary">'''

    page = post_template
    page = page.replace("{{HEADER}}", header_sub)
    page = page.replace("{{FOOTER}}", footer_sub)
    page = page.replace("{{META}}", meta)
    page = page.replace("{{TITLE}}", f"{post['title']} — Nailed & Inspired")
    page = page.replace("{{TAG}}", post["tag"])
    page = page.replace("{{POST_TITLE}}", post["title"])
    page = page.replace("{{DATE_DISPLAY}}", post["date_display"])
    page = page.replace("{{READ_TIME}}", post["read_time"])
    page = page.replace("{{BODY}}", body_html)
    page = page.replace("{{PRODUCTS}}", products_html)

    out_path = os.path.join(BLOG_DIR, f"{post['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path


def build_index(posts, index_template, header_top, footer_top):
    posts_sorted = sorted(posts, key=lambda p: p["date"], reverse=True)
    cards = []
    for post in posts_sorted:
        cards.append(f'''<a href="blog/{post['slug']}.html" class="blog-card">
        <div class="blog-thumb"></div>
        <span class="blog-tag">{post['tag']}</span>
        <span class="blog-meta">{post['date_display']} &middot; {post['read_time']}</span>
        <h3>{post['title']}</h3>
        <p>{post['excerpt']}</p>
        <span class="blog-read">Read the post</span>
      </a>''')

    page = index_template
    page = page.replace("{{HEADER}}", header_top)
    page = page.replace("{{FOOTER}}", footer_top)
    page = page.replace("{{POST_CARDS}}", "\n\n      ".join(cards))
    out_path = os.path.join(BASE_DIR, "blog.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path


def main():
    posts = load_json("posts.json")
    products = load_json("products.json")

    post_template = read_template("post_template.html")
    index_template = read_template("index_list_template.html")
    header_top = read_template("header_top.html")
    footer_top = read_template("footer_top.html")
    header_sub = read_template("header_sub.html")
    footer_sub = read_template("footer_sub.html")

    print(f"Building {len(posts)} post page(s)...")
    for post in posts:
        path = build_post_page(post, products, post_template, header_sub, footer_sub)
        print(f"  ✓ {path}")

    index_path = build_index(posts, index_template, header_top, footer_top)
    print(f"  ✓ {index_path}")
    print("Done.")


if __name__ == "__main__":
    main()