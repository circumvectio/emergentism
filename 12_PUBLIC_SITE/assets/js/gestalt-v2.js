(() => {
  "use strict";

  const root = document.documentElement;
  root.dataset.gestaltEnhanced = "true";

  const menus = Array.from(document.querySelectorAll(".g2-menu"));

  const closeMenu = (menu, restoreFocus = false) => {
    if (!menu.open) return;
    menu.removeAttribute("open");
    if (restoreFocus) menu.querySelector("summary")?.focus();
  };

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const openMenu = menus.slice().reverse().find((menu) => menu.open);
    if (openMenu) closeMenu(openMenu, true);
  });

  menus.forEach((menu) => {
    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => closeMenu(menu));
    });
  });

  const pageRail = document.querySelector("[data-g2-rail]");
  const railLinks = pageRail
    ? Array.from(pageRail.querySelectorAll("[data-g2-rail-link]"))
    : [];
  const railStops = railLinks
    .map((link) => {
      const target = document.querySelector(link.getAttribute("href"));
      return target ? { link, target } : null;
    })
    .filter(Boolean);
  const updatePageRail = () => {
    if (!pageRail || !railStops.length) return;

    const navHeight = Number.parseFloat(
      getComputedStyle(root).getPropertyValue("--g2-nav-h")
    ) || 0;
    const threshold = navHeight + pageRail.getBoundingClientRect().height + 16;
    let active = railStops[0];

    railStops.forEach((stop) => {
      if (stop.target.getBoundingClientRect().top <= threshold) active = stop;
    });

    railStops.forEach((stop) => {
      if (stop === active) stop.link.setAttribute("aria-current", "location");
      else stop.link.removeAttribute("aria-current");
    });
    pageRail.dataset.activeSection = active.link.textContent.trim();
  };

  if (pageRail && railStops.length) {
    window.addEventListener("scroll", updatePageRail, { passive: true });
    window.addEventListener("resize", updatePageRail, { passive: true });
    window.addEventListener("hashchange", updatePageRail);
    updatePageRail();
  }

  const revealTargets = Array.from(
    document.querySelectorAll("[data-g2-reveal], [data-g2-reveal-group], [data-g2-draw]")
  );
  const reducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)");
  let emergenceObserver;

  const settle = (target) => {
    target.dataset.g2Emergence = "settled";
  };

  const prepareGroups = () => {
    document.querySelectorAll("[data-g2-reveal-group]").forEach((group) => {
      Array.from(group.children).forEach((item, index) => {
        item.dataset.g2RevealItem = "";
        item.style.setProperty("--g2-order", String(Math.min(index, 6)));
      });
    });
  };

  const prepareDrawings = () => {
    document.querySelectorAll("[data-g2-draw]").forEach((drawing) => {
      const paths = Array.from(
        drawing.querySelectorAll(".actual-line, .possible-line, .evidence-line")
      );
      paths.forEach((path, index) => {
        try {
          path.dataset.g2Path = "";
          path.style.setProperty("--g2-path-length", String(Math.ceil(path.getTotalLength())));
          path.style.setProperty("--g2-path-order", String(index));
        } catch (_error) {
          path.removeAttribute("data-g2-path");
        }
      });
    });
  };

  const configureEmergence = () => {
    emergenceObserver?.disconnect();

    if (!revealTargets.length) {
      root.dataset.gestaltMotion = "static";
      return;
    }

    if (reducedMotion?.matches) {
      root.dataset.gestaltMotion = "reduced";
      revealTargets.forEach(settle);
      return;
    }

    if (!("IntersectionObserver" in window)) {
      root.dataset.gestaltMotion = "static";
      revealTargets.forEach(settle);
      return;
    }

    root.dataset.gestaltMotion = "active";
    emergenceObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.dataset.g2Emergence = "visible";
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -6%", threshold: 0.12 }
    );

    revealTargets
      .filter((target) => target.dataset.g2Emergence !== "settled")
      .forEach((target) => emergenceObserver.observe(target));
  };

  prepareGroups();
  prepareDrawings();
  configureEmergence();
  reducedMotion?.addEventListener?.("change", configureEmergence);
})();
