# Lex TL;DR

This is a small, GitHub Pages-compatible Jekyll blog for concise summaries of Lex Fridman podcast episodes, with support for adding other podcasters later. Each Markdown post is one variant of a logical summary. The shared `article_id` and `article_title` in front matter let Liquid group language or format variants on the home page and show related links on every summary page. A summary can also belong to a podcaster collection through `collection_id`. The sample `Ship Small` article demonstrates English and Chinese editions inside the first collection.

This intentionally has no CMS, database, user accounts, comments, scheduled publishing, custom domain, or custom application server.

## One-time GitHub Pages setup

1. Push this repository's default branch to GitHub.
2. In **Settings → Pages**, choose deployment from that branch and the repository **root**.
3. Set `url` and `baseurl` in `_config.yml` for the chosen repository URL.

The current configuration publishes this project repository at `https://allenlsy.github.io/lex-tldr/`. If the repository is renamed to `allenlsy.github.io` for a root user site, change `baseurl` to an empty string.

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
collection_id: practice-notes
language: es
spec:
  - short
  - audio
variant_rank: 5
permalink: /articles/ship-small/es/short-audio/
---

Write the variant here.
```

Use the language and ordered specs that describe the body (`en`/`cn` for language and values such as `short`, `long`, `guide`, or `audio` for specs). A one-item list such as `[short]` produces `short`; `[long, guide]` produces `long-guide`. Keep the list order stable because it defines the URL. Omit `spec` when language is the only distinction and end the permalink after the language, such as `/articles/ship-small/cn/`. Keep ranks unique so the related list has a predictable order. The shared ID automatically creates one home-page article group and links every related variant on each post. Give every variant of one logical article the same `collection_id`.

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

## Git publishing workflow

For each change, create a branch, add the post and metadata, run `bundle exec jekyll build`, and use `bundle exec jekyll serve` to preview it. Commit the validated change, push the branch, review/merge it into the configured deployment branch, and push that branch. Check the root URL `https://<account>.github.io/` and the GitHub Pages deployment status. Ordinary Git pushes drive publication; there is no scheduled publishing automation.
