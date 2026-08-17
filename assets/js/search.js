(() => {
  const script = document.currentScript;
  const form = document.querySelector(".search-page-form");
  const input = document.querySelector("#search-query");
  const status = document.querySelector("#search-status");
  const results = document.querySelector("#search-results");

  if (!script || !form || !input || !status || !results) return;

  const indexUrl = script.dataset.searchIndex;
  const entriesPromise = fetch(indexUrl).then((response) => {
    if (!response.ok) throw new Error(`Search index returned ${response.status}`);
    return response.json();
  });

  const normalize = (value) => value.normalize("NFKC").toLocaleLowerCase();

  const resultElement = (entry) => {
    const item = document.createElement("li");
    item.className = "search-result";

    const meta = document.createElement("p");
    meta.className = "search-result-meta";
    meta.textContent = `${entry.language.toUpperCase()} · ${entry.language_name} / ${entry.date}`;

    const heading = document.createElement("h2");
    const link = document.createElement("a");
    link.href = entry.url;
    link.textContent = entry.title;
    heading.append(link);

    const excerpt = document.createElement("p");
    excerpt.className = "search-result-excerpt";
    excerpt.textContent = entry.excerpt;

    item.append(meta, heading, excerpt);
    return item;
  };

  const runSearch = async (query) => {
    const trimmedQuery = query.trim();
    results.replaceChildren();

    if (!trimmedQuery) {
      status.textContent = "Enter a guest, topic, or phrase.";
      return;
    }

    status.textContent = "Searching…";

    try {
      const entries = await entriesPromise;
      const terms = normalize(trimmedQuery).split(/\s+/).filter(Boolean);
      const matches = entries.filter((entry) => {
        const searchable = normalize(
          `${entry.title} ${entry.article_title} ${entry.excerpt} ${entry.content}`
        );
        return terms.every((term) => searchable.includes(term));
      });

      const fragment = document.createDocumentFragment();
      matches.forEach((entry) => fragment.append(resultElement(entry)));
      results.append(fragment);
      status.textContent = `${matches.length} result${matches.length === 1 ? "" : "s"} for “${trimmedQuery}”.`;
    } catch (_error) {
      status.textContent = "Search is temporarily unavailable. Please try again.";
    }
  };

  let timer;
  input.addEventListener("input", () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => runSearch(input.value), 120);
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const url = new URL(window.location.href);
    const query = input.value.trim();
    if (query) url.searchParams.set("q", query);
    else url.searchParams.delete("q");
    window.history.replaceState({}, "", url);
    runSearch(query);
  });

  const initialQuery = new URLSearchParams(window.location.search).get("q") || "";
  input.value = initialQuery;
  runSearch(initialQuery);
})();
