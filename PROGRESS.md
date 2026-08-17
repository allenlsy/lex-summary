# Progress

Last updated: 2026-08-16

## Completed and already published

- Custom domain migration to `https://lextldr.com/`, including the root-domain canonical URLs, sitemap, robots metadata, and repository documentation.
- Podcast-summary SEO metadata, multilingual canonical and `hreflang` links, JSON-LD, and static bilingual search.
- Pagination for 10, 20, and 50 logical podcast episodes per page.
- Localized Chinese titles and linked alternate-language titles on listing pages.

## Current uncommitted work

- Article header cleanup: removed the redundant edition number and language eyebrow; the title uses the reclaimed space.
- Article metadata, header, and reading column now share the same left edge.
- Removed the redundant bottom “Choose another edition” panel. Other-language links remain in the article metadata.
- Added a system-aware light/dark theme with a persistent header toggle in `assets/js/theme.js`.
- Added a responsive article heading tree in `assets/js/post-toc.js`:
  - Rendered as a sticky navigation rail on the left side of the article page.
  - Builds from rendered Markdown `h2` and `h3` headings.
  - Is collapsible above the content on smaller screens.
  - Highlights the section currently in view.
  - Automatically hides on articles without Markdown headings.

## Browser verification completed

Runtime behavior verified with the harness browser against the local preview:

- Episode 416 CN (36 headings): the tree renders all 36 items with a heading id assigned to each, sits strictly left of the content column (`minmax(11rem, 13rem)` rail first in the `.post-body` grid), stays sticky with the divider on its right edge, and the `details` is open by default on desktop.
- Scroll tracking: the current-section marker follows the topmost heading in the 8–28% viewport band while scrolling and ends on the final section at page bottom.
- Link click: updates `location.hash` and moves `aria-current`; on small screens the tree closes after navigating.
- Mobile (390 px): tree renders above the content, `details` starts closed, rail is static with no divider; opening the summary and clicking a link closes it again.
- Episode 456 CN (no headings): the tree stays `hidden` with zero items.
- Headingless articles keep the full-width reading column: `post-toc.js` adds a `no-toc` class to `.post-body` when no headings exist, and `.post-body.no-toc` restores the single full-width column. Without this, the grid auto-placed `.post-content` into the 11–13rem rail track (the tree stayed hidden but the content rendered ~208px wide). The heading-slug regex no longer uses `\p{L}\p{N}` Unicode property escapes, which throw a `SyntaxError` in Safari before 16.4 and broke the whole script.
- Theme toggle: click flips `data-theme`, persists to `localStorage`, and the saved theme survives reload; control label, icon, and `aria-pressed` update accordingly.

## Verification completed for the uncommitted work

- `sh tests/collection_links_test.sh`
- `bundle exec jekyll build`
- `node --check assets/js/post-toc.js`
- `node --check assets/js/theme.js`
- `git diff --check`

## Files currently changed or added

- `AGENTS.md`
- `_layouts/default.html`
- `_layouts/post.html`
- `assets/css/style.css`
- `assets/js/post-toc.js` (new)
- `assets/js/theme.js` (new)
- `tests/collection_links_test.sh`

No part of this current work has been committed or pushed.
