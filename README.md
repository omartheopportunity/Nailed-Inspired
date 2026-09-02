# Nailed & Inspired

Website + blog for Nailed & Inspired.

**Everything lives in one flat folder, plus a single `data` folder.** There is
no `blog/` or `templates/` folder to worry about — that was the exact thing
that broke last time (folders got flattened during upload, causing 404s).
Every page is now its own file sitting right next to `index.html`.

**You never need to install or run anything on your computer.** Every post is
added by editing a file directly on github.com, then clicking "Commit
changes." GitHub Actions builds the actual pages for you automatically.

## Structure

```
index.html               Home page (edit directly)
blog.html                 Journal index — AUTO-GENERATED, don't hand-edit
post-<slug>.html           One file per blog post — AUTO-GENERATED, don't hand-edit
style.css                  Shared stylesheet used by every page
logo.png                   The logo image used by every page
data/posts.json            Every blog post lives here — EDIT THIS TO ADD POSTS
data/products.json         Every digital product lives here — EDIT THIS TO ADD/CHANGE PRODUCTS
generate_site.py           The generator script — runs automatically, you don't run it
.github/workflows/         The automation that runs the generator for you
```

## Adding a new post (entirely on github.com, no software needed)

1. In your repo on GitHub, click into `data` → `posts.json`
2. Click the pencil (✏️) icon in the top right to edit
3. Copy one existing post object (everything between one `{` and its matching
   `}`), paste it right after the opening `[` at the top, and add a comma
   after the `}` you pasted
4. Edit the fields on your pasted copy:
   - `slug` — unique, lowercase, hyphens only, no spaces (this becomes the
     filename `post-your-slug.html` and the URL)
   - `title`, `tag`, `date` (YYYY-MM-DD), `date_display`, `read_time`, `excerpt`
   - `body` — a list of text blocks:
     - plain text = a paragraph
     - `"## Heading"` = a subheading
     - `"> Quote"` = a pull-quote
     - `*word*` = italic emphasis
   - `products` — a list of product IDs from `data/products.json` (or `[]`)
   - `image` — a direct link to the pin image (right-click the pin on
     Pinterest → "Copy Image Address" — must end in `.jpg`/`.png`, not a
     pinterest.com page link). Leave `""` for no image.
5. Scroll down, click **"Commit changes"**
6. Wait about a minute — check the **Actions** tab in your repo for a green
   checkmark. Your new post is now live at `/post-your-slug.html`

If the JSON has a typo (a missing comma or quote), the Actions tab shows a
red X instead — click into it to see the error, or paste your edited
`posts.json` into Claude and ask it to check the syntax.

## Adding or updating a product

Same idea: open `data/products.json` on GitHub, click ✏️, add a new product
or change a `url`/`price`/`name` on an existing one, commit. Every post that
references that product ID updates automatically.

## Deploying

1. Push/upload this repo to GitHub — drag the **contents** of this folder in
   (not a folder containing it), so `index.html` sits at the repo root
2. In Vercel: **Add New Project → Import** this repo
3. Framework preset: **Other** (plain static HTML, no build command)
4. Deploy — Vercel auto-redeploys every time GitHub Actions commits new pages

Once you have your live domain, edit `generate_site.py` on GitHub, find the
`DOMAIN = "https://YOUR-DOMAIN.com"` line near the top, update it to your
real URL, and commit — this fixes the share/social preview links on every
post.

## If a page 404s after deploying

Check your GitHub repo's file list: `index.html`, `blog.html`, `style.css`,
`logo.png`, and every `post-*.html` file should all sit at the **same
level** — none of them should be nested inside a folder (other than the
`data` folder, which is supposed to be a folder). If something looks nested
that shouldn't be, delete it and re-upload.
