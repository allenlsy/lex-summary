# AGENTS.md

## Project purpose

Lex TL;DR is a small Jekyll blog that publishes concise, readable summaries of long-form podcast episodes. The initial focus is the Lex Fridman Podcast; the information architecture must remain able to add other popular podcasters later.

Keep public copy centered on this purpose. Avoid generic positioning such as a journal about ideas, making, or multiple forms unless it directly explains podcast summaries. The homepage should make three points clear:

1. The site summarizes long podcast conversations.
2. Lex Fridman is the first podcaster covered.
3. Other podcasters may be added later.

The production repository is `allenlsy/lex-tldr`, and GitHub Pages serves it at `https://lextldr.com/`.

## Architecture

- This is a static GitHub Pages-compatible Jekyll site. Do not introduce a CMS, database, user-account system, or application server without an explicit requirement.
- `_posts/` contains published summary variants.
- `_drafts/` contains unpublished fixtures or work in progress. `_drafts/spec-routing-example.md` exists to test ordered multi-value `spec` routing; do not publish it accidentally.
- `_layouts/` contains the shared shell and post presentation.
- `_data/collections.yml` defines the collection links displayed as podcasters.
- `collections/` contains collection landing pages.
- `index.html` is the first homepage summary page; `page/*/index.html` contains the remaining static pagination routes.
- `_includes/summary_index.html` renders the shared paginated episode list, and `_data/summary_pages.yml` defines its routes.
- `_includes/seo.html` renders canonical, social, multilingual, and JSON-LD metadata; `jekyll-sitemap` generates the public sitemap.
- `search.html`, `search.json`, and `assets/js/search.js` provide static bilingual full-text search; keep search GitHub Pages-compatible and client-side.
- `assets/js/post-toc.js` progressively builds the article heading tree from rendered `h2` and `h3` elements; articles without headings must not show an empty navigation.
- `assets/js/theme.js` controls the persistent light/dark theme toggle; the first visit follows the operating-system preference and the early inline setup prevents a color flash.
- `assets/css/style.css` is the site stylesheet.
- `CNAME` must remain `lextldr.com`, and `_config.yml` must keep `url: "https://lextldr.com"` with an empty `baseurl` while the custom domain is active.

The repository also contains SSSF automation under `adws/` and related recipes in `justfile`. The `new-post` recipe is the blog-specific exception. Keep other blog work independent from SSSF unless the task explicitly concerns that machinery.

Homepage pagination operates on logical episodes after grouping variants by `article_id`, never on individual language or spec variants. It offers 20 and 50 episodes per page, with 20 as the default. `_data/summary_page_sizes.yml` defines the choices, and `_data/summary_pages.yml` defines their static routes. When the episode count outgrows one of those route sets, add its next page file with the matching `summary_page` and `summary_page_size` front matter.

Keep indexable pages self-canonical. Podcast summary variants must emit reciprocal `hreflang` links, using valid BCP 47 language tags (`en` and `zh-CN`) and the English variant as `x-default` when available. Search is `noindex,follow` and excluded from the sitemap. Do not add fabricated authors, ratings, images, or other structured data that the page does not substantiate.

## Summary and variant model

Treat one podcast episode as one logical article. Every published variant of that summary must share:

- `article_id`: stable slug for the episode
- `article_title`: shared display title
- `collection_id`: podcaster collection

Each variant also has:

- `title`: localized display title for that variant; Chinese variants should use a Chinese title while `article_title` remains shared across languages. Preserve non-Chinese personal names in their original spelling; use Chinese characters for people whose original name is Chinese.
- `language`: currently use `en` and `cn` for the example
- `variant_rank`: unique, stable ordering within the logical article
- `permalink`: explicit public route
- `spec`: optional ordered YAML list for distinctions beyond language

Language display names live in `_data/languages.yml`. Templates must use the shared language-label include so every number of variants is supported and known languages show their native names.

When language is the only distinction, omit `spec` and end the URL after the language:

```yaml
language: en
variant_rank: 1
permalink: /articles/example-episode/en/
```

When `spec` is present, preserve its order and join the values with `-` in the final URL segment:

```yaml
language: en
spec:
  - short
  - audio
variant_rank: 2
permalink: /articles/example-episode/en/short-audio/
```

Most imported summaries have two variants, `en` and `cn`. Episode 440 intentionally has four variants because two distinct source summary sets were imported as ordered `short` and `long` specs. Templates must support any number of variants and render cleanly when `spec` is absent.

## Local summary imports

`scripts/import_lex_summaries.py` imports verified summary files from the local Lex Fridman iCloud folder. It must remain dry-run by default, must never modify source files, and must refuse to overwrite a different destination file. Publish only videos from the main Lex Fridman YouTube channel; the importer must continue to exclude Lex Clips sources. Keep its verified video metadata table and `tests/import_lex_summaries_test.py` in sync when adding new source summaries.

## Podcaster collections

Collections represent podcasters in the visible interface. Add a collection entry to `_data/collections.yml`, add its landing page under `collections/`, and give all related summary variants the same `collection_id`.

The first collection is displayed as `Lex Fridman Podcast` and uses the internal ID `lex-fridman`. Its `/collections/practice-notes/` route is a legacy public URL; preserve that route unless a task includes a deliberate URL migration and compatibility plan.

## Public copy and design

- Use “episode,” “summary,” “conversation,” “podcast,” “podcaster,” “language,” and “version” where appropriate.
- Do not describe summaries as unrelated articles or generic ideas in prominent UI copy.
- Keep the editorial visual theme and its responsive behavior unless redesign is requested.
- Preserve accessible navigation, semantic headings, visible focus states, and readable English and Chinese typography.
- Use Jekyll's `relative_url` for internal links so routes work locally and at the production domain root.

## Local commands

Install dependencies once:

```sh
bundle install
```

Run the regression test:

```sh
sh tests/collection_links_test.sh
```

Build the production site:

```sh
bundle exec jekyll build
```

Preview locally:

```sh
bundle exec jekyll serve
```

List the existing project recipes:

```sh
just --list
```

Create a language-only podcast summary:

```sh
just new-post "EPISODE TITLE" en
```

Preview and apply the local Lex Fridman summary import:

```sh
python3 scripts/import_lex_summaries.py
python3 scripts/import_lex_summaries.py --apply
```

The recipe derives the episode ID and URL slug from the title, assigns the next variant rank, and rejects duplicate episode-language variants. Authors must replace the generated placeholder body before publication.

## Change workflow

1. Inspect `git status` before editing. Preserve unrelated user changes.
2. For behavior changes, add or update a regression test and observe the intended failure before implementation.
3. Make the smallest coherent change.
4. Run `sh tests/collection_links_test.sh` and `bundle exec jekyll build`.
5. Run `git diff --check` and review the rendered paths or HTML relevant to the change.
6. Stage only intended files. Do not use broad staging when unrelated files exist.
7. Commit and push only when the user requests publication.

Pushing `main` triggers GitHub Pages. After publishing, verify the Pages workflow succeeds and confirm the changed routes at `https://lextldr.com/`.

## Repository hygiene

- Do not commit `_site/`; it is generated output.
- Do not commit `.env` or expose API keys and credentials.
- `dogfood-output/` is untracked QA output and must remain excluded unless explicitly requested.
- Do not change or remove historical SSSF files merely to make blog-oriented searches cleaner.
- Prefer explicit post permalinks and stable IDs over inferred routing.
