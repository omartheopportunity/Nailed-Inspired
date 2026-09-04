#!/usr/bin/env python3
"""
Nailed & Inspired — Blog Generator (flat structure)
----------------------------------------------------
Turns data/posts.json + data/products.json into:
  - blog.html            (the Journal index)
  - post-<slug>.html     (one real, shareable page per post — flat, in the
                           same folder as everything else)

Everything lives in ONE folder plus a single "data" subfolder. There is no
"blog/" or "templates/" folder to accidentally leave behind when uploading —
this was rebuilt from a nested-folder version specifically because folders
were getting flattened/lost during upload. style.css and logo.png are shared,
real files (not embedded), so browsers cache them across pages.

HOW TO ADD POSTS (the daily workflow)
  1. Open data/posts.json
  2. Copy one post object, paste it at the top of the list, give it a new
     unique "slug" (lowercase, hyphens, no spaces — this becomes the filename
     post-<slug>.html and the URL)
  3. Fill in title / tag / date / excerpt / body / products / image
     - "body" is a list of blocks. Plain text = paragraph.
       "## Heading" = subheading. "> Quote" = pull-quote.
       Wrap *word* in single asterisks for emphasis.
     - "products" is a list of product IDs from data/products.json
     - "image" is a direct link to a pin image (ending in .jpg/.png), or ""
  4. If linking a NEW digital product, add it once to data/products.json
  5. Run:  python3 generate_site.py
  6. Upload/push the updated blog.html + every post-*.html file to Vercel

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


def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def render_inline(text):
    """*word* -> <em>word</em>."""
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


HEADER = '''<header>
  <a href="index.html" class="logo logo-flex"><img src="logo.png" alt="Nailed and Inspired logo" class="logo-mark">Nailed <span>&amp;</span> Inspired</a>
  <nav>
    <ul>
      <li><a href="index.html#gap">The Shift</a></li>
      <li><a href="index.html#journey">The Journey</a></li>
      <li><a href="index.html#pain">For You</a></li>
      <li><a href="blog.html">Journal</a></li>
      <li><a href="quiz.html">Quiz</a></li>
    </ul>
  </nav>
  <a href="index.html#join" class="nav-cta">Start Your Next Chapter</a>
</header>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="index.html" class="logo logo-flex"><img src="logo.png" alt="Nailed and Inspired logo" class="logo-mark">Nailed <span>&amp;</span> Inspired</a>
        <p>Beauty is the beginning. Becoming is the mission.</p>
      </div>
      <ul class="footer-links">
        <li><a href="index.html#gap">The Shift</a></li>
        <li><a href="index.html#journey">The Journey</a></li>
        <li><a href="index.html#pain">For You</a></li>
        <li><a href="blog.html">Journal</a></li>
        <li><a href="quiz.html">Quiz</a></li>
        <li><a href="index.html#join">Community</a></li>
      </ul>
    </div>
    <div class="footer-bottom">&copy; Nailed &amp; Inspired &mdash; part of the R3UP ecosystem.</div>
  </div>
</footer>
'''

SHARE_JS = '''<script>
function copyPostLink(btn){
  navigator.clipboard.writeText(window.location.href).then(function(){
    var original = btn.textContent;
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(function(){ btn.textContent = original; btn.classList.remove("copied"); }, 1800);
  });
}
document.addEventListener("DOMContentLoaded", function(){
  var url = encodeURIComponent(window.location.href);
  var title = encodeURIComponent(document.title);
  var threads = document.getElementById("share-threads");
  if(threads){ threads.href = "https://www.threads.net/intent/post?text=" + title + "%20" + url; }
  var x = document.getElementById("share-x");
  if(x){ x.href = "https://twitter.com/intent/tweet?text=" + title + "&url=" + url; }
});
</script>
'''


def head(title, meta):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{meta}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="grain"></div>
{HEADER}
'''


def build_post_page(post, products):
    body_html = render_body(post["body"])
    products_html = render_products(post.get("products", []), products)
    image_url = post.get("image", "").strip()

    cover_html = f'<img class="post-cover" src="{image_url}" alt="{html_lib.escape(post["title"])}">' if image_url else ""
    twitter_card = "summary_large_image" if image_url else "summary"
    og_image_tag = f'<meta property="og:image" content="{image_url}">' if image_url else ""

    meta = f'''<meta name="description" content="{html_lib.escape(post['excerpt'])}">
<meta property="og:title" content="{html_lib.escape(post['title'])} \u2014 Nailed & Inspired">
<meta property="og:description" content="{html_lib.escape(post['excerpt'])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{DOMAIN}/post-{post['slug']}.html">
{og_image_tag}
<meta name="twitter:card" content="{twitter_card}">'''

    page = head(f"{post['title']} \u2014 Nailed & Inspired", meta)
    page += f'''
<section class="post-hero">
  <div class="wrap">
    <span class="blog-tag">{post['tag']}</span>
    <h1>{post['title']}</h1>
    <p class="post-meta">{post['date_display']} &middot; {post['read_time']}</p>
    {cover_html}
  </div>
</section>

<section class="post-body">
  <div class="wrap">
    {body_html}
  </div>
</section>

{products_html}

<section>
  <div class="wrap" style="max-width:720px;">
    <div class="share-row">
      <span class="label">SHARE THIS POST</span>
      <button class="share-btn" onclick="copyPostLink(this)">Copy Link</button>
      <a class="share-btn" id="share-threads" href="#" target="_blank" rel="noopener">Threads</a>
      <a class="share-btn" id="share-x" href="#" target="_blank" rel="noopener">X</a>
    </div>
    <div class="post-nav-back"><a href="blog.html">&larr; Back to The Journal</a></div>
  </div>
</section>

{SHARE_JS}{FOOTER}
</body>
</html>'''

    out_path = os.path.join(BASE_DIR, f"post-{post['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path


def build_index(posts):
    posts_sorted = sorted(posts, key=lambda p: p["date"], reverse=True)
    cards = []
    for post in posts_sorted:
        image_url = post.get("image", "").strip()
        thumb_inner = f'<img src="{image_url}" alt="{html_lib.escape(post["title"])}">' if image_url else ""
        cards.append(f'''<a href="post-{post['slug']}.html" class="blog-card">
        <div class="blog-thumb">{thumb_inner}</div>
        <span class="blog-tag">{post['tag']}</span>
        <span class="blog-meta">{post['date_display']} &middot; {post['read_time']}</span>
        <h3>{post['title']}</h3>
        <p>{post['excerpt']}</p>
        <span class="blog-read">Read the post</span>
      </a>''')

    meta = '''<meta name="description" content="The Nailed & Inspired journal — nail inspiration, self-image, confidence, and community for the woman building her next chapter.">
<meta property="og:title" content="The Journal — Nailed & Inspired">
<meta property="og:description" content="Nail inspiration, and everything it opens up.">
<meta property="og:type" content="website">'''

    page = head("The Journal \u2014 Nailed & Inspired", meta)
    page += f'''
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow-line"><span class="rule"></span><span>THE JOURNAL</span></div>
    <h1>Nail inspo, and everything it opens up.</h1>
    <p class="lede">Design ideas, self-image, confidence, and the rooms worth being in &mdash; the same arc the community walks, in article form.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="blog-grid" id="post-grid">
      {"".join(cards)}
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>'''

    out_path = os.path.join(BASE_DIR, "blog.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path


def main():
    posts = load_json("posts.json")
    products = load_json("products.json")

    print(f"Building {len(posts)} post page(s)...")
    for post in posts:
        path = build_post_page(post, products)
        print(f"  \u2713 {os.path.basename(path)}")

    index_path = build_index(posts)
    print(f"  \u2713 {os.path.basename(index_path)}")
    print("Done.")


if __name__ == "__main__":
    main()
