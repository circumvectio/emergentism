(() => {
  const root = document.documentElement;
  const buttons = document.querySelectorAll(".theme-toggle");
  const stored = window.localStorage.getItem("emergentism-theme");

  if (stored === "light") {
    root.dataset.theme = "light";
  } else {
    delete root.dataset.theme;
  }

  function syncButtons() {
    const isLight = root.dataset.theme === "light";
    buttons.forEach((button) => {
      button.textContent = isLight ? "Dark" : "Light";
      button.setAttribute("aria-label", isLight ? "Switch to dark theme" : "Switch to light theme");
      button.setAttribute("aria-pressed", String(isLight));
    });
  }

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      if (root.dataset.theme === "light") {
        delete root.dataset.theme;
        window.localStorage.setItem("emergentism-theme", "dark");
      } else {
        root.dataset.theme = "light";
        window.localStorage.setItem("emergentism-theme", "light");
      }
      syncButtons();
    });
  });

  syncButtons();
})();
