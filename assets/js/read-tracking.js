(function () {
  "use strict";

  var STORAGE_KEY = "readArticles";

  function readSet() {
    try {
      var value = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return Array.isArray(value) ? value : [];
    } catch (error) {
      return [];
    }
  }

  function saveSet(ids) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(ids)); } catch (error) {}
  }

  function markRead(id) {
    var ids = readSet();
    if (ids.indexOf(id) !== -1) return;
    ids.push(id);
    saveSet(ids);
  }

  // Article page: expose a manual read toggle persisted to localStorage
  var article = document.querySelector("article.post[data-article-id]");
  if (article) {
    var articleId = article.getAttribute("data-article-id");
    var toggle = article.querySelector("[data-read-toggle]");
    if (toggle && articleId) {
      toggle.checked = readSet().indexOf(articleId) !== -1;
      toggle.addEventListener("change", function () {
        if (toggle.checked) {
          markRead(articleId);
        } else {
          var ids = readSet().filter(function (id) { return id !== articleId; });
          saveSet(ids);
        }
      });
    }
    return;
  }

  // Listing pages: mark cards for episodes already read
  var cards = document.querySelectorAll("article.article-card[data-article-id]");
  if (!cards.length) return;
  var read = readSet();
  Array.prototype.forEach.call(cards, function (card) {
    var id = card.getAttribute("data-article-id");
    if (read.indexOf(id) === -1) return;
    var link = card.querySelector(".article-summary h2 a");
    if (!link) return;
    var mark = document.createElement("span");
    mark.className = "read-mark";
    mark.textContent = "✓";
    mark.setAttribute("aria-label", "Read");
    mark.setAttribute("data-tooltip", "Read");
    link.insertBefore(mark, link.firstChild);
  });
}());
