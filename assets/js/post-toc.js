(function () {
  "use strict";

  var toc = document.querySelector("[data-post-toc]");
  var content = document.querySelector(".post-content");
  if (!toc || !content) return;

  var headings = Array.prototype.slice.call(content.querySelectorAll("h2, h3"));
  if (!headings.length) return;

  var list = toc.querySelector("[data-post-toc-list]");
  var details = toc.querySelector("[data-post-toc-details]");
  var usedIds = {};
  var linksById = {};
  var currentParent = null;

  function headingId(heading, index) {
    var base = heading.id || heading.textContent
      .trim()
      .toLowerCase()
      .replace(/[^\w\u3400-\u4DBF\u4E00-\u9FFF]+/g, "-")
      .replace(/^-|-$/g, "") || "section-" + (index + 1);
    var candidate = base;
    var suffix = 2;

    while (usedIds[candidate] || (document.getElementById(candidate) && document.getElementById(candidate) !== heading)) {
      candidate = base + "-" + suffix;
      suffix += 1;
    }

    usedIds[candidate] = true;
    heading.id = candidate;
    return candidate;
  }

  headings.forEach(function (heading, index) {
    var id = headingId(heading, index);
    var item = document.createElement("li");
    var link = document.createElement("a");

    item.className = "post-toc-item post-toc-level-" + heading.tagName.toLowerCase();
    link.href = "#" + encodeURIComponent(id);
    link.textContent = heading.textContent.trim();
    link.title = heading.textContent.trim();
    item.appendChild(link);
    linksById[id] = link;

    if (heading.tagName === "H3" && currentParent) {
      var childList = currentParent.querySelector(".post-toc-children");
      if (!childList) {
        childList = document.createElement("ol");
        childList.className = "post-toc-children";
        currentParent.appendChild(childList);
      }
      childList.appendChild(item);
    } else {
      list.appendChild(item);
      currentParent = heading.tagName === "H2" ? item : null;
    }
  });

  toc.hidden = false;
  details.open = window.matchMedia("(min-width: 79.01rem)").matches;

  function markCurrent(id) {
    Object.keys(linksById).forEach(function (key) {
      if (key === id) linksById[key].setAttribute("aria-current", "location");
      else linksById[key].removeAttribute("aria-current");
    });
  }

  markCurrent(headings[0].id);

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      var visible = entries
        .filter(function (entry) { return entry.isIntersecting; })
        .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
      if (visible.length) markCurrent(visible[0].target.id);
    }, { rootMargin: "-8% 0px -72% 0px", threshold: 0 });

    headings.forEach(function (heading) { observer.observe(heading); });
  }

  list.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link) return;
    markCurrent(decodeURIComponent(link.hash.slice(1)));
    if (window.matchMedia("(max-width: 79rem)").matches) details.open = false;
  });
}());
