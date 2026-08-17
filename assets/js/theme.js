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

  function systemTheme() {
    return systemPreference.matches ? "dark" : "light";
  }

  // The user's choice is "light", "dark", or "system"; missing storage means "system"
  function currentChoice() {
    var saved = savedTheme();
    return saved === "light" || saved === "dark" || saved === "system" ? saved : "system";
  }

  function nextChoice(choice) {
    if (choice === "light") return "dark";
    if (choice === "dark") return "system";
    return "light";
  }

  function updateControl(choice) {
    var next = nextChoice(choice);
    var nextLabel = next === "system" ? "Auto" : next.charAt(0).toUpperCase() + next.slice(1);
    var iconChar = next === "dark" ? "◐" : next === "system" ? "◑" : "☀";
    var pressed = choice === "dark" || (choice === "system" && systemPreference.matches);
    toggle.setAttribute("aria-label", "Use " + next + " theme");
    toggle.setAttribute("title", "Use " + next + " theme");
    toggle.setAttribute("aria-pressed", pressed ? "true" : "false");
    label.textContent = nextLabel;
    icon.textContent = iconChar;
  }

  function applyTheme(choice, persist) {
    var effective = choice === "system" ? systemTheme() : choice;
    root.setAttribute("data-theme", effective);
    updateControl(choice);
    if (persist) {
      try { localStorage.setItem("theme", choice); } catch (error) {}
    }
  }

  applyTheme(currentChoice(), false);

  toggle.addEventListener("click", function () {
    applyTheme(nextChoice(currentChoice()), true);
  });

  systemPreference.addEventListener("change", function () {
    var saved = savedTheme();
    if (saved !== "light" && saved !== "dark") {
      applyTheme("system", false);
    }
  });
}());
