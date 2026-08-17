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
  - Floats at the far left edge of the viewport on desktop (`position: fixed`, vertically centered) and no longer occupies a grid column: the reading column keeps its full 64rem width.
  - On viewports below 79rem it folds back to the collapsible block above the content; the `details` default-open state follows the same breakpoint.
  - Header, metadata, reading column, and comments share the same left edge; comments moved inside the article container so the floating tree never covers them.
  - Builds from rendered Markdown `h2` and `h3` headings, highlights the section in view, and hides on headingless articles.
- Homepage pagination now offers 20 and 50 episodes per page (20 is the default); the 10-per-page option and its `/page/3/` and `/per-page/20/` routes were removed. `/` is the first 20-per-page page and `/page/2/` the second.

## Browser verification completed

Runtime behavior verified with the harness browser against the local preview:

- Episode 416 CN (36 headings): the tree renders all 36 items with a heading id assigned to each, sits strictly left of the content column (`minmax(11rem, 13rem)` rail first in the `.post-body` grid), stays sticky with the divider on its right edge, and the `details` is open by default on desktop.
- Scroll tracking: the current-section marker follows the topmost heading in the 8–28% viewport band while scrolling and ends on the final section at page bottom.
- Link click: updates `location.hash` and moves `aria-current`; on small screens the tree closes after navigating.
- Mobile (390 px): tree renders above the content, `details` starts closed, rail is static with no divider; opening the summary and clicking a link closes it again.
- Episode 456 CN (no headings): the tree stays `hidden` with zero items and the reading column stays full-width.
- Desktop floating nav: at 1440/1365 px the tree sits at `left: 24px` (208px wide), the reading column starts at 272px and is 1024px wide, nothing overlaps, and header/meta/comments share the 272px left edge; at 1280 px the column is 984px. The tree stays fixed while scrolling.
- Folded state at 1248 px: tree is static above the content, `details` starts closed, content is centered 1024px and aligned with the header.
- Pagination: `/` renders 20 episode cards, `/page/2/` renders 8 (production has 28 episodes; the test suite builds with drafts and asserts 20/9/29), `/per-page/50/` renders 28. The size chooser offers only 20 and 50, marking the active one with `aria-current`.
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
