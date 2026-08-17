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

  // Article page: read toggles persisted to localStorage, synced across variants
  var article = document.querySelector("article.post[data-article-id]");
  if (article) {
    var articleId = article.getAttribute("data-article-id");
    var toggles = article.querySelectorAll("[data-read-toggle]");
    if (toggles.length && articleId) {
      var isRead = readSet().indexOf(articleId) !== -1;
      Array.prototype.forEach.call(toggles, function (toggle) {
        toggle.checked = isRead;
        toggle.addEventListener("change", function () {
          var nowChecked = toggle.checked;
          Array.prototype.forEach.call(toggles, function (other) { other.checked = nowChecked; });
          if (nowChecked) {
            markRead(articleId);
          } else {
            saveSet(readSet().filter(function (id) { return id !== articleId; }));
          }
        });
      });
      // Articles without a heading tree get a floating toggle in the nav area
      var toc = article.querySelector(".post-toc");
      var floatToggle = article.querySelector(".read-toggle-float");
      if (toc && toc.hidden && floatToggle) floatToggle.hidden = false;
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
