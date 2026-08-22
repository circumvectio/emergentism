(() => {
  const root = document.documentElement;
  root.dataset.gestaltEnhanced = "true";

  const menu = document.querySelector(".g2-menu");
  if (menu) {
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menu.open) {
        menu.removeAttribute("open");
        menu.querySelector("summary")?.focus();
      }
    });
    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => menu.removeAttribute("open"));
    });
  }

})();
