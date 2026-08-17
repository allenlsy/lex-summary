(function () {
  "use strict";

  var root = document.documentElement;
  var toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) return;

  var label = toggle.querySelector("[data-theme-label]");
  var icon = toggle.querySelector("[data-theme-icon]");
  var systemPreference = window.matchMedia("(prefers-color-scheme: dark)");

  function savedTheme() {
    try { return localStorage.getItem("theme"); } catch (error) { return null; }
  }

  function updateControl(theme) {
    var isDark = theme === "dark";
    var action = isDark ? "light" : "dark";
    toggle.setAttribute("aria-label", "Use " + action + " theme");
    toggle.setAttribute("title", "Use " + action + " theme");
    toggle.setAttribute("aria-pressed", isDark ? "true" : "false");
    label.textContent = isDark ? "Light" : "Dark";
    icon.textContent = isDark ? "☀" : "◐";
  }

  function applyTheme(theme, persist) {
    root.setAttribute("data-theme", theme);
    updateControl(theme);
    if (persist) {
      try { localStorage.setItem("theme", theme); } catch (error) {}
    }
  }

  updateControl(root.getAttribute("data-theme") || "light");

  toggle.addEventListener("click", function () {
    applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true);
  });

  systemPreference.addEventListener("change", function (event) {
    if (!savedTheme()) applyTheme(event.matches ? "dark" : "light", false);
  });
}());
