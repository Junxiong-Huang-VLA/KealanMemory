(function () {
  const state = {
    allSkills: [],
    allRoles: [],
    currentSearch: "",
    activeSkillCategory: null,
    activeRoleCategory: null,
    opsLoaded: false,
    toastTimer: null,
    editFiles: [],
    currentEditPath: "",
    lastPreviewKey: "",
  };

  const titles = {
    home: "Overview",
    memory: "Memory",
    editor: "Editor",
    skills: "Skills",
    roles: "Roles",
    ops: "Ops Panel",
  };

  const $ = (id) => document.getElementById(id);

  document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    init();
  });

  function bindEvents() {
    document.querySelectorAll("[data-tab]").forEach((button) => {
      button.addEventListener("click", () => showTab(button.dataset.tab));
    });

    $("overlay").addEventListener("click", closeDetail);
    $("detail-close").addEventListener("click", closeDetail);
    $("search-input").addEventListener("input", handleSearch);
    $("project-select").addEventListener("change", loadMemory);
    $("copy-memory").addEventListener("click", copyMemory);
    $("edit-file-select").addEventListener("change", loadEditFile);
    $("reload-edit-file").addEventListener("click", loadEditFile);
    $("edit-content").addEventListener("input", markDiffStale);
    $("preview-diff").addEventListener("click", previewDiff);
    $("save-edit-file").addEventListener("click", saveEditFile);
    $("refresh-health").addEventListener("click", loadHealth);
    $("history-search-btn").addEventListener("click", loadHistory);
    $("history-query").addEventListener("keydown", (event) => {
      if (event.key === "Enter") loadHistory();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && $("detail-panel").classList.contains("open")) {
        closeDetail();
      }
    });
  }

  async function init() {
    try {
      const [skills, roles, projects, focus, editable] = await Promise.all([
        fetchJson("/api/skills"),
        fetchJson("/api/roles"),
        fetchJson("/api/projects"),
        fetchJson("/api/focus"),
        fetchJson("/api/editable-files"),
      ]);

      state.allSkills = Array.isArray(skills) ? skills : [];
      state.allRoles = Array.isArray(roles) ? roles : [];

      setText("stat-skills", state.allSkills.length);
      setText("stat-roles", state.allRoles.length);
      setText("stat-projects", Array.isArray(projects) ? projects.length : 0);
      setText("badge-skills", state.allSkills.length);
      setText("badge-roles", state.allRoles.length);

      const focusContent = String(focus && focus.content ? focus.content : "").trim();
      setText("focus-block", focusContent ? preview(focusContent, 800) : "No active focus content.");

      populateProjects(Array.isArray(projects) ? projects : []);
      populateEditableFiles(editable.files || []);
      buildFilters("skill-filters", state.allSkills, "skill");
      buildFilters("role-filters", state.allRoles, "role");
      renderCards("skills-grid", state.allSkills);
      renderCards("roles-grid", state.allRoles);
      loadMemory();
      loadHealthBadge();
    } catch (error) {
      showToast("Failed to load dashboard data.", "error");
      setText("focus-block", "Load failed. Please retry later.");
      setError("skills-grid", "Skill data failed to load.");
      setError("roles-grid", "Role data failed to load.");
      setText("context-box", "Memory context failed to load.");
      setText("diff-output", "Editable file list failed to load.");
      setText("ctx-chars", "... chars");
      console.error(error);
    }
  }

  async function fetchJson(url, options) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(`${url} returned ${response.status}`);
      error.data = data;
      throw error;
    }
    return data;
  }

  function populateProjects(projects) {
    const select = $("project-select");
    projects.forEach((project) => {
      const option = document.createElement("option");
      option.value = project;
      option.textContent = project;
      select.appendChild(option);
    });
  }

  function populateEditableFiles(files) {
    state.editFiles = Array.isArray(files) ? files : [];
    const select = $("edit-file-select");
    select.innerHTML = "";

    state.editFiles.forEach((file) => {
      const option = document.createElement("option");
      option.value = file.path;
      option.textContent = file.label || file.path;
      select.appendChild(option);
    });

    if (state.editFiles.length) {
      select.value = state.editFiles[0].path;
      loadEditFile();
    } else {
      setText("diff-title", "No editable files");
      setText("diff-state", "empty");
      $("edit-content").value = "";
      $("edit-content").disabled = true;
      setText("diff-output", "No whitelisted editable files are available.");
    }
  }

  function buildFilters(containerId, items, type) {
    const categories = ["All", ...new Set(items.map((item) => item.category).filter(Boolean))];
    const container = $(containerId);
    container.innerHTML = "";

    categories.forEach((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `filter-chip${category === "All" ? " active" : ""}`;
      button.textContent = category;
      button.addEventListener("click", () => {
        container.querySelectorAll(".filter-chip").forEach((chip) => chip.classList.remove("active"));
        button.classList.add("active");
        const nextCategory = category === "All" ? null : category;
        if (type === "skill") {
          state.activeSkillCategory = nextCategory;
          filterSkills();
        } else {
          state.activeRoleCategory = nextCategory;
          filterRoles();
        }
      });
      container.appendChild(button);
    });
  }

  function filterSkills() {
    let items = state.activeSkillCategory
      ? state.allSkills.filter((skill) => skill.category === state.activeSkillCategory)
      : state.allSkills;
    if (state.currentSearch) items = items.filter((skill) => matchesSearch(skill));
    renderCards("skills-grid", items);
  }

  function filterRoles() {
    let items = state.activeRoleCategory
      ? state.allRoles.filter((role) => role.category === state.activeRoleCategory)
      : state.allRoles;
    if (state.currentSearch) items = items.filter((role) => matchesSearch(role));
    renderCards("roles-grid", items);
  }

  function matchesSearch(item) {
    const query = state.currentSearch.toLowerCase();
    const fields = [item.name, item.id, item.category, item.description].map((value) => String(value || "").toLowerCase());
    return fields.some((field) => field.includes(query));
  }

  function renderCards(containerId, items) {
    const grid = $(containerId);
    grid.innerHTML = "";

    if (!items.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "No matching results.";
      grid.appendChild(empty);
      return;
    }

    items.forEach((item) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "card";
      card.addEventListener("click", () => openDetail(item));

      const top = document.createElement("span");
      top.className = "card-top";

      const name = document.createElement("span");
      name.className = "card-name";
      name.textContent = item.name || item.id || "";

      const badge = document.createElement("span");
      badge.className = "cat-badge";
      badge.textContent = item.category || "Other";

      const description = document.createElement("span");
      description.className = "card-desc";
      description.textContent = item.description || "";

      const arrow = document.createElement("span");
      arrow.className = "card-arrow";
      arrow.innerHTML = '<svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';

      top.append(name, badge);
      card.append(top, description, arrow);
      grid.appendChild(card);
    });
  }

  function openDetail(item) {
    setText("detail-cat", item.category || "");
    setText("detail-title", item.name || item.id || "");
    $("detail-content").innerHTML = renderMd(item.body || item.description || "");
    $("detail-panel").classList.add("open");
    $("overlay").classList.add("open");
    $("detail-panel").setAttribute("aria-hidden", "false");
    $("detail-close").focus();
  }

  function closeDetail() {
    $("detail-panel").classList.remove("open");
    $("overlay").classList.remove("open");
    $("detail-panel").setAttribute("aria-hidden", "true");
  }

  async function loadMemory() {
    const project = $("project-select").value;
    setText("context-box", "Loading...");
    setText("ctx-chars", "... chars");

    try {
      const data = await fetchJson(`/api/memory?project=${encodeURIComponent(project)}`);
      const context = String(data.context || "");
      setText("context-box", context);
      setText("ctx-chars", `${context.length.toLocaleString()} chars`);
    } catch (error) {
      setText("context-box", "Memory context failed to load.");
      showToast("Memory context failed to load.", "error");
      console.error(error);
    }
  }

  async function copyMemory() {
    const project = $("project-select").value;
    const text = $("context-box").textContent;

    try {
      const data = await fetchJson("/api/copy-memory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project }),
      });
      if (data.ok) {
        showToast(`Copied ${Number(data.chars || 0).toLocaleString()} chars.`);
        return;
      }
    } catch (error) {
      console.warn(error);
    }

    try {
      await navigator.clipboard.writeText(text);
      showToast("Copied to clipboard.");
    } catch (error) {
      try {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
        showToast("Copied with fallback mode.");
      } catch (fallbackError) {
        showToast("Copy failed. Select the text manually.", "error");
        console.error(fallbackError);
      }
    }
  }

  async function loadEditFile() {
    const path = $("edit-file-select").value;
    if (!path) return;

    $("edit-content").disabled = true;
    $("edit-content").value = "Loading...";
    setText("diff-title", path);
    setText("diff-state", "loading");
    setText("diff-output", "Diff preview is cleared. Edit the file and preview before saving.");
    setText("save-health-status", "Save has not run.");
    setText("save-health-output", "");
    state.currentEditPath = path;
    state.lastPreviewKey = "";

    try {
      const data = await fetchJson(`/api/edit-file?path=${encodeURIComponent(path)}`);
      state.currentEditPath = data.path || path;
      $("edit-content").value = data.content || "";
      $("edit-content").disabled = false;
      setText("diff-title", state.currentEditPath);
      setText("diff-state", "loaded");
    } catch (error) {
      $("edit-content").value = "";
      setText("diff-state", "error");
      setText("diff-output", error.data && error.data.error ? error.data.error : "Failed to load editable file.");
      showToast("Editable file failed to load.", "error");
      console.error(error);
    }
  }

  function markDiffStale() {
    if (state.lastPreviewKey) {
      setText("diff-state", "stale");
    }
  }

  async function previewDiff() {
    const path = state.currentEditPath || $("edit-file-select").value;
    const content = $("edit-content").value;
    if (!path) return;

    setText("diff-state", "previewing");
    setText("diff-output", "Generating diff...");

    try {
      const data = await fetchJson("/api/diff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path, content }),
      });
      state.lastPreviewKey = previewKey(path, content);
      setText("diff-state", data.changed ? "changed" : "no changes");
      setText("diff-output", data.diff || "No changes.");
    } catch (error) {
      state.lastPreviewKey = "";
      setText("diff-state", "error");
      setText("diff-output", error.data && error.data.error ? error.data.error : "Diff generation failed.");
      showToast("Diff preview failed.", "error");
      console.error(error);
    }
  }

  async function saveEditFile() {
    const path = state.currentEditPath || $("edit-file-select").value;
    const content = $("edit-content").value;
    if (!path) return;

    if (state.lastPreviewKey !== previewKey(path, content)) {
      showToast("Preview the current diff before saving.", "error");
      await previewDiff();
      return;
    }

    setText("diff-state", "saving");
    setText("save-health-status", "Saving and running health check...");
    setText("save-health-output", "");

    try {
      const data = await fetchJson("/api/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path, content }),
      });
      state.lastPreviewKey = previewKey(path, content);
      setText("diff-state", data.changed ? "saved" : "saved, unchanged");
      setText("diff-output", data.diff || "No changes.");
      setSaveHealth(data.health || {});
      showToast("Saved. Health check completed.");
      loadHealthBadge();
      if (path === "context/active_focus.md") {
        setText("focus-block", preview(content, 800) || "No active focus content.");
      }
    } catch (error) {
      setText("diff-state", "error");
      setSaveHealth({ ok: false, summary: error.data && error.data.error ? error.data.error : "Save failed.", output: "" });
      showToast("Save failed.", "error");
      console.error(error);
    }
  }

  function setSaveHealth(data) {
    const ok = Boolean(data.ok);
    const status = $("save-health-status");
    status.className = `health-status ${ok ? "ok" : "fail"}`;
    status.textContent = data.summary || (ok ? "Health check passed." : "Health check failed.");
    setText("save-health-output", data.output || "");
  }

  async function loadOps() {
    if (state.opsLoaded) return;
    state.opsLoaded = true;
    await Promise.all([loadRouting(), loadHealth(), loadHistory()]);
  }

  async function loadRouting() {
    try {
      const data = await fetchJson("/api/routing");
      const summary = data.summary || {};
      const routing = data.routing || {};
      const routes = routing.routes || routing.intents || [];
      const projects = data.projects || [];

      setText("routing-count", `${summary.route_count || routes.length} routes`);
      setText("project-status-count", `${projects.length} projects`);
      renderRoutes(Array.isArray(routes) ? routes : []);
      renderProjectStatus(projects);
    } catch (error) {
      setText("routing-count", "failed");
      setText("project-status-count", "failed");
      setError("routing-list", "Routing map failed to load.");
      setError("project-status-list", "Project status failed to load.");
      console.error(error);
    }
  }

  function renderRoutes(routes) {
    const list = $("routing-list");
    list.innerHTML = "";
    if (!routes.length) {
      list.appendChild(emptyState("No routing entries."));
      return;
    }

    routes.forEach((route) => {
      const item = document.createElement("div");
      item.className = "route-item";

      const title = document.createElement("div");
      title.className = "route-title";
      title.textContent = route.intent || route.id || "unnamed-route";

      const desc = document.createElement("div");
      desc.className = "route-desc";
      desc.textContent = route.description || "";

      const meta = document.createElement("div");
      meta.className = "route-meta";
      meta.append(
        pill(`role: ${route.role || "none"}`),
        pill(`skills: ${(route.skills || []).join(", ") || "none"}`),
        pill(`files: ${(route.default_files || []).length}`),
      );

      item.append(title, desc, meta);
      list.appendChild(item);
    });
  }

  function renderProjectStatus(projects) {
    const list = $("project-status-list");
    list.innerHTML = "";
    if (!projects.length) {
      list.appendChild(emptyState("No projects registered."));
      return;
    }

    projects.forEach((project) => {
      const item = document.createElement("div");
      item.className = "project-status-item";

      const head = document.createElement("div");
      head.className = "project-status-head";
      const name = document.createElement("strong");
      name.textContent = project.name;
      const status = pill(project.missing && project.missing.length ? `${project.missing.length} missing` : "complete");
      status.classList.toggle("pill-danger", Boolean(project.missing && project.missing.length));
      head.append(name, status);

      const body = document.createElement("div");
      body.className = "project-status-body";
      body.textContent = preview(project.status_preview || project.next_actions_preview || "No status content.", 420);

      item.append(head, body);
      list.appendChild(item);
    });
  }

  async function loadHealthBadge() {
    try {
      const data = await fetchJson("/api/health");
      setText("badge-health", data.ok ? "ok" : "fail");
    } catch (error) {
      setText("badge-health", "fail");
    }
  }

  async function loadHealth() {
    setText("health-status", "Running health check...");
    setText("health-output", "");
    try {
      const data = await fetchJson("/api/health");
      setHealth(data);
    } catch (error) {
      setHealth(error.data || { ok: false, summary: error.message, output: "" });
    }
  }

  function setHealth(data) {
    const ok = Boolean(data.ok);
    const status = $("health-status");
    status.className = `health-status ${ok ? "ok" : "fail"}`;
    status.textContent = data.summary || (ok ? "Health check passed." : "Health check failed.");
    setText("health-output", data.output || "");
    setText("badge-health", ok ? "ok" : "fail");
  }

  async function loadHistory() {
    const query = $("history-query").value.trim();
    const results = $("history-results");
    results.innerHTML = "";
    results.appendChild(emptyState("Searching..."));

    try {
      const data = await fetchJson(`/api/history?q=${encodeURIComponent(query)}`);
      renderHistory(data.results || []);
    } catch (error) {
      setError("history-results", "History search failed.");
      console.error(error);
    }
  }

  function renderHistory(items) {
    const results = $("history-results");
    results.innerHTML = "";
    if (!items.length) {
      results.appendChild(emptyState("No history entries found."));
      return;
    }

    items.forEach((entry) => {
      const item = document.createElement("div");
      item.className = "history-item";
      const title = document.createElement("div");
      title.className = "history-title";
      title.textContent = entry.title || entry.file;
      const file = document.createElement("div");
      file.className = "history-file";
      file.textContent = entry.file;
      const snippet = document.createElement("pre");
      snippet.className = "history-snippet";
      snippet.textContent = entry.snippet || "";
      item.append(title, file, snippet);
      results.appendChild(item);
    });
  }

  function showTab(name) {
    document.querySelectorAll(".tab-content").forEach((tab) => tab.classList.remove("active"));
    document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));

    $(`tab-${name}`).classList.add("active");
    $(`nav-${name}`).classList.add("active");
    setText("page-title", titles[name] || "");

    const showSearch = name === "skills" || name === "roles";
    $("search-wrap").classList.toggle("visible", showSearch);
    if (!showSearch) {
      $("search-input").value = "";
      state.currentSearch = "";
    }
    if (name === "ops") loadOps();
  }

  function previewKey(path, content) {
    return `${path}\n${content}`;
  }

  function handleSearch() {
    state.currentSearch = $("search-input").value.trim();
    const active = document.querySelector(".tab-content.active");
    if (active && active.id === "tab-skills") filterSkills();
    if (active && active.id === "tab-roles") filterRoles();
  }

  function showToast(message, type) {
    const toast = $("toast");
    setText("toast-msg", message);
    toast.classList.toggle("error", type === "error");
    toast.classList.add("show");
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2800);
  }

  function renderMd(markdown) {
    let html = esc(markdown);
    html = html.replace(/```[\w]*\n([\s\S]*?)```/g, "<pre><code>$1</code></pre>");
    html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");
    html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
    html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>[\s\S]*?<\/li>\n?)+/g, (list) => `<ul>${list}</ul>`);
    html = html.split("\n\n").map((block) => {
      if (/^<(h[1-3]|ul|pre|table)/.test(block.trim())) return block;
      return `<p>${block}</p>`;
    }).join("");
    return html.replace(/<p><\/p>/g, "");
  }

  function esc(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function preview(value, maxLength) {
    const text = String(value || "").trim();
    return text.length > maxLength ? `${text.slice(0, maxLength)}\n...` : text;
  }

  function pill(text) {
    const node = document.createElement("span");
    node.className = "pill";
    node.textContent = text;
    return node;
  }

  function emptyState(message) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = message;
    return empty;
  }

  function setText(id, value) {
    $(id).textContent = value;
  }

  function setError(containerId, message) {
    const container = $(containerId);
    container.innerHTML = "";
    const error = document.createElement("div");
    error.className = "error-state";
    error.textContent = message;
    container.appendChild(error);
  }
})();
