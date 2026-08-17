# Lex TL;DR

This is a small, GitHub Pages-compatible Jekyll blog for concise summaries of Lex Fridman podcast episodes, with support for adding other podcasters later. Each Markdown post is one variant of a logical summary. The shared `article_id` and `article_title` in front matter let Liquid group language or format variants on the home page and show related links on every summary page. A summary can also belong to a podcaster collection through `collection_id`. The sample episode demonstrates English and Chinese editions inside the first collection.

This intentionally has no CMS, database, user accounts, scheduled publishing, or custom application server. Post comments are provided by the client-side Disqus embed.

## One-time GitHub Pages setup

1. Push this repository's default branch to GitHub.
2. In **Settings → Pages**, choose deployment from that branch and the repository **root**.
3. Configure `lextldr.com` as the custom domain and enable HTTPS.

The production site is published at `https://lextldr.com/`. The repository keeps `CNAME` set to `lextldr.com`, with `url: "https://lextldr.com"` and an empty `baseurl` in `_config.yml` so public routes start at the domain root.

## Local preview and build

Install Ruby, Bundler, and a supported Jekyll/GitHub Pages environment, then run:

```sh
bundle install
bundle exec jekyll serve
```

Open the displayed local URL (normally `http://localhost:4000/`). For a production-style check, run:

```sh
bundle exec jekyll build
```

The generated site is in `_site/`.

## Add or relate a variant

Create a language-only summary from the command line:

```sh
just new-post "456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom" en
```

The recipe creates a date-prefixed file under `_posts/`, derives a stable episode slug and permalink from the title, assigns the next `variant_rank`, and omits `spec`. Run the same title with another language such as `cn` to create a related language variant. It refuses to create the same episode-language combination twice. Review the generated front matter and replace the placeholder body before publishing.

Create a date-prefixed Markdown file in `_posts/`, for example `2025-02-01-ship-small-es-short-audio.md`. To relate it to the existing logical article, retain its `article_id` and `article_title`; to start a new logical article, choose a new ID and title. Set a unique, stable `variant_rank` within that article. `spec` is an ordered YAML list describing the edition. Join its values with `-` for the final permalink segment:

```yaml
---
layout: post
title: "Ship Small: Spanish Short Guide"
date: 2025-02-01 09:00:00 +0000
article_id: ship-small
article_title: "Ship Small"
collection_id: lex-fridman
language: es
spec:
  - short
  - audio
variant_rank: 5
permalink: /articles/ship-small/es/short-audio/
---

Write the variant here.
```

Use the language and ordered specs that describe the body (`en`/`cn` for language and values such as `short`, `long`, `guide`, or `audio` for specs). A one-item list such as `[short]` produces `short`; `[long, guide]` produces `long-guide`. Keep the list order stable because it defines the URL. Omit `spec` when language is the only distinction and end the permalink after the language, such as `/articles/ship-small/cn/`. Keep ranks unique so the related list has a predictable order. The shared ID automatically creates one home-page article group and links every related variant on each post. An article may have any number of language variants. Give every variant of one logical article the same `collection_id`.

Native language names are defined in `_data/languages.yml` and displayed after each language code, such as `EN · English` and `CN · 中文`. Add a mapping there when introducing another language. Codes without a mapping still render safely as their uppercase code.

## Import local Lex Fridman summaries

The repository includes a safe importer for the summary Markdown files stored in the local iCloud folder. It defaults to a dry run:

```sh
python3 scripts/import_lex_summaries.py
```

Review the complete plan, then create the missing Jekyll posts with:

```sh
python3 scripts/import_lex_summaries.py --apply
```

The importer only reads the source directory. It preflights every destination before writing, refuses to overwrite different files, skips byte-identical duplicates and Lex Clips sources, and is safe to run again after a successful import. Verified Lex Fridman channel URLs and publication dates are maintained in the script's metadata table.

## Add a collection

Collections are listed in `_data/collections.yml`. Add one stable ID, display title, URL, and description:

```yaml
- id: design-systems
  title: Design Systems
  url: /collections/design-systems/
  description: Notes on building coherent interfaces at scale.
```

Then create `collections/design-systems.html` using `collections/practice-notes.html` as the template, changing its `title`, `collection_id`, and `permalink`. Assign an article by adding `collection_id: design-systems` to every one of its variants. The collection automatically appears in the masthead, its landing page groups related editions by `article_id`, and each article links back to the collection.

Run the collection regression test after changing collection metadata or URLs:

```sh
sh tests/collection_links_test.sh
```

## Disqus comments

Individual post pages load the Disqus Universal Embed using the `lex-tldr` forum shortname configured in `_config.yml`. Each thread uses the post's canonical absolute URL and explicit permalink as its stable identifier. Change `disqus.shortname` if the site moves to another registered Disqus forum.

## Git publishing workflow

For each change, create a branch, add the post and metadata, run `bundle exec jekyll build`, and use `bundle exec jekyll serve` to preview it. Commit the validated change, push the branch, review/merge it into the configured deployment branch, and push that branch. Check the root URL `https://<account>.github.io/` and the GitHub Pages deployment status. Ordinary Git pushes drive publication; there is no scheduled publishing automation.
