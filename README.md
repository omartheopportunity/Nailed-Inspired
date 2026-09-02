# Nailed & Inspired

Website + blog for Nailed & Inspired.

**You never need to install or run anything on your computer.** Every post is added
by editing a file directly on github.com, then clicking "Commit changes." A robot
(GitHub Actions) builds the actual pages for you automatically.

## Structure

```
index.html               Home page (edit directly)
blog.html                 Journal index — AUTO-GENERATED, don't hand-edit
blog/*.html                Individual post pages — AUTO-GENERATED, don't hand-edit
data/posts.json           Every blog post lives here — EDIT THIS TO ADD POSTS
data/products.json        Every digital product lives here — EDIT THIS TO ADD/CHANGE PRODUCTS
templates/                 Page layout used by the generator (don't touch unless changing design)
generate_site.py           The generator script — runs automatically, you don't run it
.github/workflows/         The automation that runs the generator for you
```

## Adding a new post (entirely on github.com, no software needed)

1. In your repo on GitHub, click into `data` → `posts.json`
2. Click the pencil (✏️) icon in the top right to edit
3. Copy one existing post object (everything between one `{` and its matching `}`),
   paste it right after the opening `[` at the top, and add a comma after the `}`
   you pasted
4. Edit the fields on your pasted copy:
   - `slug` — unique, lowercase, hyphens only, no spaces (this becomes the URL)
   - `title`, `tag`, `date` (YYYY-MM-DD), `date_display`, `read_time`, `excerpt`
   - `body` — a list of text blocks:
     - plain text = a paragraph
     - `"## Heading"` = a subheading
     - `"> Quote"` = a pull-quote
     - `*word*` = italic emphasis
   - `products` — a list of product IDs from `data/products.json` (or `[]` for none)
5. Scroll down, click **"Commit changes"**
6. Wait about a minute — check the **Actions** tab in your repo, you'll see it running,
   then a green checkmark. Your new post is now live at `/blog/your-slug.html`

If you make a typo in the JSON (a missing comma or quote), the Actions tab will show
a red X instead of a checkmark — click into it to see what it's complaining about, or
just paste your edited posts.json into Claude and ask it to check the syntax.

## Adding or updating a product

Same idea: open `data/products.json` on GitHub, click ✏️, add a new product or change
a `url`/`price`/`name` on an existing one, commit. Every post that references that
product ID updates automatically — no need to touch individual post files.

## Deploying

1. Push/upload this repo to GitHub
2. In Vercel: **Add New Project → Import** this repo
3. Framework preset: **Other** (plain static HTML, no build command)
4. Deploy — Vercel will auto-redeploy every time GitHub Actions commits new pages

Once you have your live domain, edit `generate_site.py` on GitHub (same ✏️-and-commit
process), find the `DOMAIN = "https://YOUR-DOMAIN.com"` line near the top, and update
it to your real URL. Commit — this fixes the share/social preview links on every post.
