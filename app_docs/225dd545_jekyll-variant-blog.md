# GitHub Pages variant blog

## What changed

A standalone, GitHub Pages-compatible Jekyll blog was added at the repository root alongside the existing SSSF material. It models each Markdown post as a variant of a logical article: shared `article_id` and `article_title` metadata groups related posts, while `language`, `format`, and `variant_rank` describe and order the variants. The site has no CMS, database, accounts, comments, scheduled publishing, custom domain, or custom application server.

The sample `Ship Small` article contains four linked variants: English short, English long, Chinese short, and Chinese long. The home page groups these as one logical article and lists all four links; every post page renders navigation to its related variants.

## Files carrying the change

- `Gemfile` pins GitHub Pages tooling and Ruby-compatible dependency constraints for local builds.
- `_config.yml` defines the site metadata, `baseurl: ""`, the `<account>.github.io` URL placeholder, Markdown/permalink settings, and generated-site exclusions.
- `index.html` groups `site.posts` by `article_id` and lists each group’s variants.
- `_layouts/default.html` provides the shared HTML shell and root link; `_layouts/post.html` displays article metadata and sorted related-variant links.
- `_posts/2025-01-10-ship-small.md`, `_posts/2025-01-11-ship-small-long.md`, `_posts/2025-01-12-ship-small-zh-short.md`, and `_posts/2025-01-13-ship-small-zh-long.md` provide the four sample variants with explicit `/articles/ship-small/<language>/<format>/` permalinks.
- `assets/css/style.css` supplies responsive styling, readable English/Chinese typography, and visible link focus states.
- `README.md` documents setup, authoring metadata, local commands, and the Git publishing workflow.
- `specs/225dd545_jekyll-variant-blog.md` records the implementation scope and verification checklist.

## Use and verification

For deployment, rename or create the GitHub repository as `<account>.github.io`, replace the `url` placeholder in `_config.yml`, push the default branch, and configure GitHub Pages to deploy that branch from the repository root. This produces `https://<account>.github.io/` rather than a project-site subpath.

For local checking, install Ruby/Bundler and run:

```sh
bundle install
bundle exec jekyll serve
bundle exec jekyll build
```

Preview the displayed local URL and inspect `_site/`. A new variant belongs in a date-prefixed file under `_posts/` with a shared `article_id`/`article_title` for an existing article, a unique stable `variant_rank`, `language`, `format`, and an explicit unique permalink. A new `article_id` starts a new logical article. The documented Git loop is branch, author metadata/content, build and preview, commit, push, merge into the deployment branch, push, then check the root Pages URL and deployment status.

The diff adds the build and preview instructions but does not record an executed build result; run `bundle exec jekyll build` to verify the current environment.