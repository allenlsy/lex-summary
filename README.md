# Variant Notes

This is a small, GitHub Pages-compatible Jekyll blog. Each Markdown post is one variant of a logical article. The shared `article_id` and `article_title` in front matter let Liquid group variants on the home page and show related links on every article page. The sample `Ship Small` article demonstrates English and Chinese, short and long forms.

This intentionally has no CMS, database, user accounts, comments, scheduled publishing, custom domain, or custom application server.

## One-time GitHub Pages setup

1. Create (or rename) the GitHub repository to **`<account>.github.io`**, replacing `<account>` with the GitHub user or organization account name.
2. Push this repository's default branch to GitHub.
3. In **Settings → Pages**, choose deployment from that branch and the repository **root** (or use the repository's configured Pages branch/root option).

That exact repository name makes this a user/organization site at `https://<account>.github.io/`. A project repository instead normally produces a `/project-name/` URL. Replace the placeholder `url` in `_config.yml` with the real account URL before publishing.

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

Create a date-prefixed Markdown file in `_posts/`, for example `2025-02-01-ship-small-es-short.md`. To relate it to the existing logical article, retain its `article_id` and `article_title`; to start a new logical article, choose a new ID and title. Set a unique, stable `variant_rank` within that article, and provide a unique explicit permalink:

```yaml
---
layout: post
title: "Ship Small: Spanish Short Guide"
date: 2025-02-01 09:00:00 +0000
article_id: ship-small
article_title: "Ship Small"
language: es
format: short
variant_rank: 5
permalink: /articles/ship-small/es/short/
---

Write the variant here.
```

Use the language and form that describe the body (`en`/`zh` and `short`/`long` for the common cases), and choose a new combination and permalink when adding another variant—for example `/articles/ship-small/zh/long/` or `/articles/new-idea/en/short/`. Keep ranks unique so the related list has a predictable order. The shared ID automatically creates one home-page article group and links every related variant on each post.

## Git publishing workflow

For each change, create a branch, add the post and metadata, run `bundle exec jekyll build`, and use `bundle exec jekyll serve` to preview it. Commit the validated change, push the branch, review/merge it into the configured deployment branch, and push that branch. Check the root URL `https://<account>.github.io/` and the GitHub Pages deployment status. Ordinary Git pushes drive publication; there is no scheduled publishing automation.
