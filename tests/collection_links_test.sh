#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
site_dir=$(mktemp -d "${TMPDIR:-/tmp}/variant-notes-test.XXXXXX")
trap 'rm -rf "$site_dir"' EXIT

cd "$repo_dir"

if ! grep -Fq -- '- id: lex-fridman' _data/collections.yml || \
   grep -R -Fq 'collection_id: practice-notes' _posts _drafts collections; then
  echo "FAIL: Lex Fridman content does not consistently use the lex-fridman collection ID" >&2
  exit 1
fi

echo "PASS: Lex Fridman content uses the lex-fridman collection ID"

for lex_clips_id in \
  NCNXbAFbWn8 I2ZK3ngNvvI QJ38en58Onk IQBA4aytp_U MPXUCoWeKM8 IACy_jZUkiE bzMh4b5awHw
do
  if grep -R -Fq "$lex_clips_id" _posts; then
    echo "FAIL: Lex Clips video remains published: $lex_clips_id" >&2
    exit 1
  fi
done

echo "PASS: Lex Clips videos are excluded from published posts"

bundle exec jekyll build --quiet --drafts --destination "$site_dir"

home_page="$site_dir/index.html"

for purpose_text in \
  'Podcast summaries' \
  'Lex Fridman first' \
  'more podcasters to come'
do
  if ! grep -Fq "$purpose_text" "$home_page"; then
    echo "FAIL: homepage does not communicate its podcast-summary purpose: $purpose_text" >&2
    exit 1
  fi
done

echo "PASS: homepage communicates its podcast-summary purpose"

if grep -Fq 'class="intro ' "$home_page"; then
  echo "FAIL: homepage still renders the intro section" >&2
  exit 1
fi

echo "PASS: homepage omits the intro section"

if ! awk '
  /class="section-heading"/ { in_heading = 1 }
  in_heading && /<h1>Latest summaries<\/h1>/ { found = 1; exit }
  END { exit !found }
' "$home_page"; then
  echo "FAIL: homepage section heading does not provide the page h1" >&2
  exit 1
fi

if ! grep -Fq '.section-heading h1 { margin: 0; font-size: clamp(1.5rem, 2.4vw, 2rem);' "$site_dir/assets/css/style.css"; then
  echo "FAIL: section heading h1 does not use the compact type scale" >&2
  exit 1
fi

echo "PASS: homepage section heading uses a compact h1"

if ! awk '
  /class="article-summary"/ { in_summary = 1 }
  in_summary && /<h2>/ { saw_heading = 1 }
  in_summary && saw_heading && /class="edition-list"/ { found = 1; exit }
  END { exit !found }
' "$home_page"; then
  echo "FAIL: language chooser is not directly grouped below the article heading" >&2
  exit 1
fi

echo "PASS: homepage groups the language chooser below the article heading"

if ! grep -Fq '<h2><a href="/lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/">456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom</a></h2>' "$home_page"; then
  echo "FAIL: homepage post title does not link directly to its English version" >&2
  exit 1
fi

if ! grep -Fq 'assign title_variant = english_variant | default: representative' _includes/summary_index.html; then
  echo "FAIL: homepage post title does not fall back to the first variation" >&2
  exit 1
fi

echo "PASS: homepage post titles link to English with a first-variation fallback"

for page_spec in \
  "index.html:10" \
  "page/2/index.html:10" \
  "page/3/index.html:9" \
  "per-page/20/index.html:20" \
  "per-page/20/page/2/index.html:9" \
  "per-page/50/index.html:29"
do
  page_path=${page_spec%:*}
  expected_count=${page_spec##*:}
  rendered_page="$site_dir/$page_path"

  if [ ! -f "$rendered_page" ]; then
    echo "FAIL: summary pagination page was not generated: $page_path" >&2
    exit 1
  fi

  actual_count=$(grep -Foc 'class="article-card"' "$rendered_page")
  if [ "$actual_count" -ne "$expected_count" ]; then
    echo "FAIL: $page_path renders $actual_count episode cards; expected $expected_count" >&2
    exit 1
  fi

  if grep -Fq 'class="article-index"' "$rendered_page"; then
    echo "FAIL: $page_path still renders the obsolete post index block" >&2
    exit 1
  fi
done

echo "PASS: homepage pagination splits logical episodes into ten-card pages"
echo "PASS: summary pages omit the obsolete post index block"

if ! grep -Fq '.article-summary { display: grid; grid-template-columns: minmax(0, 1fr) minmax(18rem, .65fr);' "$site_dir/assets/css/style.css" || \
   ! grep -Fq '.article-summary .edition-list { grid-column: 2; grid-row: 3;' "$site_dir/assets/css/style.css" || \
   ! grep -Fq '.article-excerpt { grid-column: 1; grid-row: 3;' "$site_dir/assets/css/style.css"; then
  echo "FAIL: summary cards do not reuse the former index space with a balanced content grid" >&2
  exit 1
fi

echo "PASS: summary cards reuse the former index space with a balanced content grid"

if ! grep -Fq 'aria-label="Episodes per page"' "$home_page" || \
   ! grep -Fq 'aria-current="page">10</a>' "$home_page" || \
   ! grep -Fq 'href="/lex-tldr/per-page/20/">20</a>' "$home_page" || \
   ! grep -Fq 'href="/lex-tldr/per-page/50/">50</a>' "$home_page" || \
   ! grep -Fq 'aria-current="page">20</a>' "$site_dir/per-page/20/index.html"; then
  echo "FAIL: summary index does not offer accessible 10, 20, and 50 episode page sizes" >&2
  exit 1
fi

echo "PASS: summary index offers 10, 20, and 50 episode page sizes"

if ! grep -Fq 'aria-label="Summary pages"' "$home_page" || \
   ! grep -Fq 'href="/lex-tldr/page/2/"' "$home_page" || \
   ! grep -Fq 'aria-current="page">2</a>' "$site_dir/page/2/index.html" || \
   ! grep -Fq 'href="/lex-tldr/page/3/"' "$site_dir/page/2/index.html"; then
  echo "FAIL: summary pagination does not provide accessible baseurl-aware navigation" >&2
  exit 1
fi

echo "PASS: homepage pagination provides accessible baseurl-aware navigation"

if ! grep -Fq 'href="/lex-tldr/collections/practice-notes/"' "$home_page"; then
  echo "FAIL: homepage does not link to the Practice Notes collection with the project base URL" >&2
  exit 1
fi

echo "PASS: homepage links to the Practice Notes collection"

collection_page="$site_dir/collections/practice-notes/index.html"

if [ ! -f "$collection_page" ]; then
  echo "FAIL: Practice Notes collection page was not generated" >&2
  exit 1
fi

if grep -Fq '>Journal</a>' "$collection_page"; then
  echo "FAIL: collection navigation still includes the redundant Journal link" >&2
  exit 1
fi

echo "PASS: collection navigation omits the redundant Journal link"

for edition_path in \
  /lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/ \
  /lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/cn/ \
  /lex-tldr/articles/spec-routing-example/en/long-guide/
do
  if ! grep -Fq "href=\"$edition_path\"" "$collection_page"; then
    echo "FAIL: collection page does not link to $edition_path" >&2
    exit 1
  fi
done

echo "PASS: collection page links to every article edition"

if grep -Fq 'class="collection-entry-index"' "$collection_page"; then
  echo "FAIL: collection entries still render the obsolete index block" >&2
  exit 1
fi

echo "PASS: collection entries omit the obsolete index block"

if ! grep -Fq '<h2><a href="/lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/">456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom</a></h2>' "$collection_page"; then
  echo "FAIL: collection entry title does not link directly to its English version" >&2
  exit 1
fi

echo "PASS: collection entry title links directly to its English version"

for language_page in "$home_page" "$collection_page"
do
  for language_label in 'EN · English' 'CN · 中文'
  do
    if ! grep -Fq "$language_label" "$language_page"; then
      echo "FAIL: page does not display the native language label: $language_label" >&2
      exit 1
    fi
  done
done

echo "PASS: listing pages display native language names"

if ! awk '
  /class="collection-heading"/ { in_heading = 1 }
  in_heading && /<h1>/ { saw_title = 1 }
  in_heading && saw_title && /class="collection-intro"/ { found = 1; exit }
  END { exit !found }
' "$collection_page"; then
  echo "FAIL: collection intro is not grouped below the collection heading" >&2
  exit 1
fi

echo "PASS: collection intro sits below the collection heading"

if ! awk '
  /class="collection-entry-copy"/ { in_entry = 1 }
  in_entry && /<h2>/ { saw_heading = 1 }
  in_entry && saw_heading && /class="collection-entry-meta"/ { found = 1; exit }
  END { exit !found }
' "$collection_page"; then
  echo "FAIL: collection entry does not place metadata below its title" >&2
  exit 1
fi

echo "PASS: collection entry places metadata below its title"

if ! grep -Fq '.collection-entry-copy h2 { margin: 0 0 1.5rem; font-size: clamp(1.65rem, 2.6vw, 2.25rem);' "$site_dir/assets/css/style.css" || \
   ! grep -Fq 'white-space: nowrap;' "$site_dir/assets/css/style.css"; then
  echo "FAIL: collection entry title is not constrained to one line" >&2
  exit 1
fi

echo "PASS: collection entry title uses the compact single-line treatment"

article_page="$site_dir/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/index.html"
cn_article_page="$site_dir/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/cn/index.html"

if grep -Fq '>Journal</a>' "$article_page"; then
  echo "FAIL: article navigation still includes the redundant Journal link" >&2
  exit 1
fi

echo "PASS: article navigation omits the redundant Journal link"

if ! grep -Fq 'EN · English' "$article_page" || \
   ! grep -Fq 'CN · 中文' "$article_page" || \
   ! grep -Fq 'CN · 中文' "$cn_article_page"; then
  echo "FAIL: article pages do not display native language names" >&2
  exit 1
fi

echo "PASS: article pages display native language names"

if ! grep -Fq 'class="post-collection" href="/lex-tldr/collections/practice-notes/"' "$article_page"; then
  echo "FAIL: article does not identify and link back to its collection" >&2
  exit 1
fi

echo "PASS: article links back to its collection"

if ! awk '
  /class="post-meta"/ { in_meta = 1 }
  in_meta && /class="post-other-versions"/ { found = 1; exit }
  END { exit !found }
' "$article_page" || ! grep -Fq 'href="/lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/cn/"' "$article_page"; then
  echo "FAIL: article metadata does not link to another language version" >&2
  exit 1
fi

echo "PASS: article metadata links to another language version"

episode_article_page="$article_page"

if ! grep -Fq '<span>Original episode</span>' "$episode_article_page" || \
   ! grep -Fq 'class="post-original-link" href="https://www.youtube.com/watch?v=u321m25rKXc">Original Link' "$episode_article_page"; then
  echo "FAIL: article does not render its original_link metadata" >&2
  exit 1
fi

echo "PASS: article renders its original_link metadata"

if grep -Fq '<aside' "$episode_article_page"; then
  echo "FAIL: article content still renders an aside" >&2
  exit 1
fi

echo "PASS: article content omits the aside"

if ! grep -Fq '.post-body { max-width: 64rem;' "$site_dir/assets/css/style.css"; then
  echo "FAIL: article content does not reclaim the former aside space" >&2
  exit 1
fi

echo "PASS: article content reclaims the former aside space"

if ! grep -Fq '.post-heading h1 { max-width: 62rem; margin: 0; font-size: clamp(2.75rem, 6vw, 5.25rem);' "$site_dir/assets/css/style.css"; then
  echo "FAIL: article heading still uses the oversized type scale" >&2
  exit 1
fi

echo "PASS: article heading uses the reduced type scale"

if ! grep -Fq 'id="disqus_thread"' "$article_page" || \
   ! grep -Fq "https://lex-tldr.disqus.com/embed.js" "$article_page"; then
  echo "FAIL: article does not load the lex-tldr Disqus forum" >&2
  exit 1
fi

if ! grep -Fq 'this.page.url = "https://allenlsy.github.io/lex-tldr/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/";' "$article_page" || \
   ! grep -Fq 'this.page.identifier = "/articles/456-ukraine-war-peace-putin-trump-nato-and-freedom/en/";' "$article_page"; then
  echo "FAIL: Disqus does not use the canonical article URL and stable permalink identifier" >&2
  exit 1
fi

echo "PASS: article configures a stable Disqus thread"

if ! awk '
  /class="post-content"/ { saw_content = 1 }
  saw_content && /id="disqus_thread"/ { saw_comments = 1 }
  saw_comments && /class="variants"/ { found = 1; exit }
  END { exit !found }
' "$article_page"; then
  echo "FAIL: Disqus comments are not placed below the article content and above version navigation" >&2
  exit 1
fi

echo "PASS: article places Disqus comments below its content"

if grep -Fq '<span>Specification</span>' "$article_page"; then
  echo "FAIL: an edition without specs renders an empty specification field" >&2
  exit 1
fi

echo "PASS: article omits empty specification metadata"

long_article_page="$site_dir/articles/spec-routing-example/en/long-guide/index.html"

if ! grep -Fq 'EN · English · LONG / GUIDE' "$long_article_page"; then
  echo "FAIL: article does not render the ordered spec list" >&2
  exit 1
fi

echo "PASS: article renders the ordered spec list"
