(function () {
  "use strict";

  const page = document.body.dataset.livingPage;
  if (!page) return;

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  async function loadData() {
    const [parityResponse, mapResponse] = await Promise.all([
      fetch("../public_semantic_parity.json", { cache: "no-store" }),
      fetch("../living-map.json", { cache: "no-store" })
    ]);
    if (!parityResponse.ok || !mapResponse.ok) throw new Error("The public research contracts could not be loaded.");
    return { parity: await parityResponse.json(), map: await mapResponse.json() };
  }

  function gapsFor(id, questions) {
    return questions.filter((question) => question.registers.includes(id));
  }

  function buildNodes(parity) {
    const levels = new Map(parity.levels.map((level) => [level.id, level]));
    const transitions = new Map();
    parity.levels.forEach((level) => {
      if (level.transition) transitions.set(level.transition.id, level.transition);
    });
    const output = [];
    const seen = new Map();
    parity.sequence.forEach((id) => {
      seen.set(id, (seen.get(id) || 0) + 1);
      const key = `${id}-${seen.get(id)}`;
      if (levels.has(id)) {
        const level = levels.get(id);
        output.push({ key, id, kind: id === "D6" || id === "D0" ? "boundary" : "register", ...level });
      } else if (transitions.has(id)) {
        const transition = transitions.get(id);
        output.push({ key, id, kind: id === "b6" ? "boundary" : "crossing", title: transition.label, subtitle: transition.evidence, tier: transition.evidence, ...transition });
      } else if (id === "r6") {
        const relation = levels.get("D6").return;
        output.push({ key, id, kind: "return", title: relation.label, subtitle: "Boundary-role comparison", source: levels.get("D6").source, summary: relation.meaning, ...relation });
      }
    });
    return output;
  }

  function sourceLabel(source) {
    return source ? `Source owner: ${source}` : "Source owner is declared in the dimension contract.";
  }

  function renderInspector(node, questions) {
    const inspector = $("#map-inspector");
    if (!inspector) return;
    inspector.replaceChildren();

    const status = element("div", "inspector-status");
    status.append(element("span", "", `${node.id} · ${node.kind}`));
    status.append(element("span", "tier", node.tier || node.evidence || "[I]"));
    inspector.append(status);
    inspector.append(element("h3", "", node.title || node.label || node.id));
    inspector.append(element("p", "subtitle", node.subtitle || "Typed public scaffold position"));

    const blocks = [];
    if (node.summary) blocks.push(["What it says", node.summary]);
    if (node.inherited) blocks.push(["Inherited account", node.inherited]);
    if (node.saturation) blocks.push(["Lower-register limit", node.saturation]);
    if (node.capability) blocks.push(["Candidate capability", node.capability]);
    if (node.recovery) blocks.push(["Recovery obligation", node.recovery]);
    if (node.prediction) blocks.push(["Discriminator", node.prediction]);
    if (node.alternatives) blocks.push(["Strong alternatives", node.alternatives]);
    if (node.boundary) blocks.push(["Boundary", node.boundary]);
    if (node.kill) blocks.push(["Kill", node.kill]);
    blocks.forEach(([heading, copy]) => {
      const block = element("section", "inspector-block");
      block.append(element("h4", "", heading));
      block.append(element("p", "", copy));
      inspector.append(block);
    });

    const source = element("p", "inspector-source", sourceLabel(node.source));
    inspector.append(source);

    const actions = element("div", "inspector-actions");
    const levelHref = /^D[0-6]$/.test(node.id) ? `../${node.id.slice(1)}/` : "../dimensions/";
    const levelLink = element("a", "", /^D[0-6]$/.test(node.id) ? `Open ${node.id}` : "Open the typed spine");
    levelLink.href = levelHref;
    actions.append(levelLink);
    if (questions.length) {
      const labLink = element("a", "", `${questions.length} open ${questions.length === 1 ? "question" : "questions"}`);
      labLink.href = `../lab/?register=${encodeURIComponent(node.id)}`;
      actions.append(labLink);
    }
    inspector.append(actions);
  }

  function renderGapCards(nodeId, questions) {
    const wall = $("#selected-gaps");
    const title = $("#selected-gaps-title");
    if (!wall || !title) return;
    const gaps = gapsFor(nodeId, questions).sort((a, b) => a.priority - b.priority);
    title.textContent = gaps.length ? `Open work touching ${nodeId}` : `${nodeId} has no directly routed open socket`;
    wall.replaceChildren();
    if (!gaps.length) {
      const empty = element("div", "gap-card");
      empty.append(element("span", "gid", "NO DIRECT SOCKET"));
      empty.append(element("h4", "", "The scaffold remains revisable."));
      empty.append(element("p", "", "Report a contradiction or propose a typed question without treating absence as completion."));
      wall.append(empty);
      return;
    }
    gaps.slice(0, 6).forEach((question) => {
      const card = element("a", "gap-card");
      card.href = `../lab/#${question.id}`;
      card.append(element("span", "gid", `${question.id} · ${question.status}`));
      card.append(element("h4", "", question.shortTitle));
      card.append(element("p", "", question.nextMilestone));
      wall.append(card);
    });
  }

  function renderMap(parity, map) {
    const rail = $("#map-rail");
    if (!rail) return;
    const nodes = buildNodes(parity);
    rail.replaceChildren();
    let selected = nodes[0];

    function select(node, button) {
      selected = node;
      $$(".map-node", rail).forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      renderInspector(node, gapsFor(node.id, map.openQuestions));
      renderGapCards(node.id, map.openQuestions);
    }

    nodes.forEach((node, index) => {
      const button = element("button", `map-node ${node.kind}`);
      button.type = "button";
      button.setAttribute("aria-pressed", String(index === 0));
      button.setAttribute("aria-label", `Inspect ${node.id}: ${node.title || node.label || node.kind}`);
      button.append(element("span", "node-id", node.id.replace("mu", "μ")));
      button.append(element("span", "node-kind", node.kind));
      const count = gapsFor(node.id, map.openQuestions).length;
      if (count) button.append(element("span", "node-gaps", `${count} open`));
      button.addEventListener("click", () => select(node, button));
      rail.append(button);
    });
    renderInspector(selected, gapsFor(selected.id, map.openQuestions));
    renderGapCards(selected.id, map.openQuestions);
  }

  function statusColor(status) {
    return {
      "ready-to-freeze": "#c99b32",
      "component-contact": "#2c7a70",
      "formal-only": "#244a8d",
      "deferred": "#765b9c"
    }[status] || "#8b8d91";
  }

  function renderQuestionCard(question) {
    const card = element("article", "question-card");
    card.id = question.id;
    card.dataset.status = question.status;
    card.dataset.registers = question.registers.join(" ");
    card.style.setProperty("--status-color", statusColor(question.status));
    const top = element("div", "question-top");
    top.append(element("span", "question-id", `${question.id} · priority ${question.priority}`));
    top.append(element("span", "status", question.status.replaceAll("-", " ")));
    card.append(top);
    card.append(element("h3", "", question.title));
    card.append(element("p", "question", question.question));
    const details = element("dl", "");
    [["Next", question.nextMilestone], ["Moves", question.moves], ["Kill", question.kill], ["Register", question.registers.join(" · ")]].forEach(([term, value]) => {
      details.append(element("dt", "", term));
      details.append(element("dd", "", value));
    });
    card.append(details);
    const actions = element("div", "card-actions");
    const contribute = element("a", "", "Prepare a contribution →");
    contribute.href = `../contribute/?question=${question.id}`;
    actions.append(contribute);
    if (question.publicIssue) {
      const issue = element("a", "", "Open preregistration ↗");
      issue.href = question.publicIssue;
      issue.target = "_blank";
      issue.rel = "noopener noreferrer";
      actions.append(issue);
    }
    card.append(actions);
    return card;
  }

  function renderLab(map) {
    const grid = $("#question-grid");
    if (!grid) return;
    const questions = [...map.openQuestions].sort((a, b) => a.priority - b.priority);
    grid.replaceChildren(...questions.map(renderQuestionCard));

    const params = new URLSearchParams(location.search);
    const register = params.get("register");
    if (register) {
      $$(".question-card", grid).forEach((card) => { card.hidden = !card.dataset.registers.split(" ").includes(register); });
      const notice = $("#lab-scope");
      if (notice) notice.textContent = `Showing questions routed through ${register}. Clear the filter to see the full research queue.`;
    }

    $$("[data-filter]").forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.dataset.filter;
        $$("[data-filter]").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
        $$(".question-card", grid).forEach((card) => { card.hidden = filter !== "all" && card.dataset.status !== filter; });
        const notice = $("#lab-scope");
        if (notice) notice.textContent = filter === "all" ? "Showing all eleven packet-complete, evidence-open questions." : `Showing ${filter.replaceAll("-", " ")} questions.`;
      });
    });
  }

  function renderContribution(map) {
    const count = $("#open-question-count");
    if (count) count.textContent = String(map.openQuestions.length);
    const modes = $("#contribution-modes");
    if (modes) {
      modes.replaceChildren(...map.contributionModes.map((mode) => {
        const card = element("article", "principle");
        card.append(element("span", "mark", mode.id.toUpperCase()));
        card.append(element("h3", "", mode.title));
        card.append(element("p", "", mode.description));
        return card;
      }));
    }
    const params = new URLSearchParams(location.search);
    const requested = params.get("question");
    if (requested) {
      const question = map.openQuestions.find((item) => item.id === requested);
      const target = $("#selected-question");
      if (target && question) target.textContent = `${question.id} selected: ${question.title}. The static release records intent only; no compute or payment is accepted here yet.`;
    }
  }

  function wireCopy() {
    $$("[data-copy-target]").forEach((button) => {
      button.addEventListener("click", async () => {
        const target = document.getElementById(button.dataset.copyTarget);
        if (!target) return;
        try {
          await navigator.clipboard.writeText(target.textContent);
          button.textContent = "Copied";
        } catch (_error) {
          button.textContent = "Select and copy";
          const range = document.createRange();
          range.selectNodeContents(target);
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
        }
      });
    });
  }

  loadData().then(({ parity, map }) => {
    if (page === "map") renderMap(parity, map);
    if (page === "lab") renderLab(map);
    if (page === "contribute") renderContribution(map);
    wireCopy();
    document.documentElement.dataset.livingMapReady = "true";
  }).catch((error) => {
    const target = $("[data-load-status]");
    if (target) {
      target.className = "load-error";
      target.textContent = `${error.message} Use the typed dimensions and Record links while the interface is unavailable.`;
    }
  });
})();
