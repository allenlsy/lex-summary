# Plan: GitHub Pages Jekyll variant blog

## Scope and approach
Create an independent, conventional Jekyll site at the repository root without altering the existing `adws/` SSSF machinery. Use the GitHub Pages gem locally so the development build matches the hosted plugin/runtime constraints. Model each published file as one variant and connect variants with shared front-matter metadata (`article_id`); render those relationships with standard Liquid filters, requiring no database, CMS, or server-side application.

## Files to add

1. **`Gemfile`**
   - Declare the `github-pages` gem (in its normal Jekyll plugin group) so `bundle exec jekyll build` and `bundle exec jekyll serve` use GitHub Pages-compatible dependencies.
   - Do not introduce non-GitHub-Pages plugins or an application runtime.

2. **`_config.yml`**
   - Configure the site title/description, Markdown engine, GitHub Pages-safe permalink behavior, and `baseurl: ""` so a user/organization site resolves at `https://<account>.github.io/` rather than under a project subpath.
   - Include a clearly marked `url`/account placeholder that the repository owner replaces with their real GitHub account before publishing.
   - Exclude SSSF/runtime-only material as needed from the generated site while leaving the machinery in place and tracked.

3. **`_layouts/default.html`** and **`_layouts/post.html`**
   - Add a minimal semantic site shell (header, root-home link, main content, footer) and a post layout with title, publication date, language, and form/length metadata.
   - In the post layout, find all `site.posts` with the current page's `article_id`, sort them by an explicit `variant_rank`, and render a “related variants” navigation list. Mark the current item accessibly and link every sibling via its generated relative URL.
   - Keep the templates within standard GitHub Pages/Jekyll Liquid capabilities; do not depend on custom plugins.

4. **`index.html`**
   - Render the blog landing page at `/`.
   - Group posts by `article_id`; for each logical article, derive a representative title/summary and list links to all of its variants, rather than treating language/format files as unrelated articles.
   - Make the page usable with the sample content and any future posts following the documented metadata contract.

5. **`assets/css/style.css`**
   - Supply a small responsive, readable stylesheet for the site shell, article metadata, article lists, and related-variant navigation. Ensure Chinese text and English text are both legible and navigation links have visible interaction/focus states.

6. **Four sample posts under `_posts/`** (one unique, date-prefixed filename per variant)
   - Add one shared logical sample article with these four combinations: English/short, English/long, Chinese/short, and Chinese/long.
   - Give all four posts the same `article_id` and shared logical `article_title`, but unique titles, content, permalinks, and ranks. Set front matter consistently: `layout: post`, `date`, `language` (`en` or `zh`), `format` (`short` or `long`), `variant_rank`, and an explicit `permalink` such as `/articles/<article-id>/en/short/`.
   - Write actual concise/expanded content appropriate to each form and Chinese content for the Chinese variants, so the example proves both dimensions rather than merely labeling duplicate files.
   - Confirm every individual post's related-variants list exposes all four variants and the home page groups them under one logical article.

7. **`README.md`**
   - Document the purpose and lightweight architecture (Jekyll posts plus front-matter relationships) and state the intentionally excluded capabilities: CMS/database/accounts/comments/scheduling/custom domain/custom server.
   - Provide the one-time GitHub setup exactly for a user or organization Pages site: create or rename the repository to **`<account>.github.io`** (substituting the actual account), push the default branch, and configure GitHub Pages to deploy that branch from the repository root. Explain that this naming is what produces the root URL `https://<account>.github.io/`, unlike a project Pages repository.
   - Document local prerequisites and repeatable commands: install dependencies with Bundler, preview with `bundle exec jekyll serve`, and production-check with `bundle exec jekyll build`.
   - Define the future-variant authoring contract: copy/create a date-prefixed `_posts` Markdown file; retain the logical article's `article_id` and `article_title`; set `language`, `format`, `variant_rank`, and a unique explicit permalink; write the variant body; and keep ranks unique/stable within that article. Include a front-matter example and naming/permalink examples for new English, Chinese, short, or long variants.
   - Describe how the shared ID creates the automatic home-page grouping and per-post related links, so authors know how to relate a new variant to an existing article versus start a new logical article.
   - Document the Git publishing loop: create a branch, add/validate the post, run the local build/preview, commit, push, merge/push to the configured deployment branch, and check the root Pages URL and GitHub Pages deployment status. Mention that ordinary Git pushes drive publication; no scheduled automation is present.

## Implementation notes

- Keep content-site paths at the root (`_posts`, `_layouts`, `_config.yml`, `index.html`, and `assets`) and do not move, modify, or couple to `adws/` or `justfile`.
- Use `relative_url` (and normal Jekyll-generated `post.url`) for internal links so local previews and the empty user-site base path behave correctly.
- Prefer explicitly authored permalinks and ranks over unsupported dynamic routing or inferred relationships; this makes language/format URLs predictable and the Liquid-only relationship behavior reliable.

## Verification

1. Run `bundle install` and then `bundle exec jekyll build`; it must exit successfully and create `_site/`.
2. Inspect the generated home page and each generated sample article page. Verify the home page has one logical sample article with four working variant links, and each of the four pages has related-variant navigation containing English/Chinese and short/long choices.
3. Run `bundle exec jekyll serve` and open the local root URL. Check layout styling, root navigation, Chinese rendering, each explicit permalink, and sibling navigation in a browser.
4. Review `README.md` against the requested workflow: it must name the repository as `<account>.github.io`, distinguish a root user/organization URL from project Pages, explain adding and relating variants, and give local preview plus Git-based publish steps.
5. After pushing to GitHub in a real account, verify Pages is configured for the default branch/root and that the deployed site is reachable at `https://<account>.github.io/` with the sample and links present.
