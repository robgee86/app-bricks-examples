// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

(() => {
  const socket = io(`${window.location.protocol}//${window.location.host}`);

  const feedPanelEl = document.getElementById("feed-panel");
  const listEl = document.getElementById("article-list");
  const emptyEl = document.getElementById("empty-state");
  const unreadCountEl = document.getElementById("unread-count");
  const unreadChipEl = document.getElementById("unread-chip");
  const markAllBtn = document.getElementById("mark-all-read");
  const connectionEl = document.getElementById("connection-status");
  const connectionLabelEl = connectionEl.querySelector(".connection-label");

  const detailEl = document.getElementById("article-detail");
  const detailTitleEl = document.getElementById("detail-title");
  const detailMetaEl = document.getElementById("detail-meta");
  const detailBodyEl = document.getElementById("detail-body");
  const detailToggleBtn = document.getElementById("detail-toggle-read");
  const backBtn = document.getElementById("back-btn");

  let articles = [];
  let selectedId = null;

  // Open sanitized links in a new tab without leaking the referrer.
  DOMPurify.addHook("afterSanitizeAttributes", (node) => {
    if (node.tagName === "A" && node.getAttribute("href")) {
      node.setAttribute("target", "_blank");
      node.setAttribute("rel", "noopener noreferrer");
    }
  });

  function setConnectionState(state, label) {
    connectionEl.dataset.state = state;
    connectionLabelEl.textContent = label;
  }

  socket.on("connect", () => setConnectionState("connected", "Live"));
  socket.on("disconnect", () => setConnectionState("disconnected", "Offline"));
  socket.io.on("reconnect_attempt", () =>
    setConnectionState("connecting", "Reconnecting")
  );
  socket.on("articles_update", (payload) => {
    articles = Array.isArray(payload?.articles) ? payload.articles : [];
    if (selectedId && !articles.some((a) => a.id === selectedId)) {
      selectedId = null;
    }
    render();
  });

  markAllBtn.addEventListener("click", () => {
    articles
      .filter((a) => !a.read)
      .forEach((a) => socket.emit("mark_read", { id: a.id }));
  });

  backBtn.addEventListener("click", () => {
    selectedId = null;
    render();
  });

  detailToggleBtn.addEventListener("click", () => {
    const article = currentSelection();
    if (!article) return;
    const next = !article.read;
    article.read = next;
    socket.emit(next ? "mark_read" : "mark_unread", { id: article.id });
    render();
  });

  function selectArticle(id) {
    selectedId = id;
    const article = articles.find((a) => a.id === id);
    if (article && !article.read) {
      article.read = true;
      socket.emit("mark_read", { id });
    }
    render();
  }

  function currentSelection() {
    return selectedId ? articles.find((a) => a.id === selectedId) : null;
  }

  function render() {
    const selection = currentSelection();
    if (selection) {
      feedPanelEl.hidden = true;
      detailEl.hidden = false;
      renderDetail(selection);
    } else {
      detailEl.hidden = true;
      feedPanelEl.hidden = false;
      renderList();
    }

    const unread = articles.filter((a) => !a.read).length;
    unreadCountEl.textContent = String(unread);
    unreadChipEl.dataset.empty = unread === 0 ? "true" : "false";
    markAllBtn.disabled = unread === 0;
  }

  function renderList() {
    if (articles.length === 0) {
      listEl.replaceChildren();
      emptyEl.hidden = false;
      return;
    }
    emptyEl.hidden = true;

    // Reconcile in place: update existing cards without detaching them, so
    // their slide-in animation never restarts (detach + reattach would replay
    // it on every refresh — the flicker). Only brand-new cards are inserted
    // (and animate); nodes move only when their order actually changes.
    const existing = new Map(
      Array.from(listEl.children).map((node) => [node.dataset.id, node])
    );
    const nextIds = new Set(articles.map((a) => a.id));

    // Remove gone cards first, so they don't sit between surviving cards and
    // force those to move (which would restart their animation).
    for (const [id, node] of existing) {
      if (!nextIds.has(id)) {
        node.remove();
        existing.delete(id);
      }
    }

    let prev = null;
    for (const article of articles) {
      let node = existing.get(article.id);
      if (node) updateArticleNode(node, article);
      else node = buildArticleNode(article);
      const ref = prev ? prev.nextSibling : listEl.firstChild;
      if (node !== ref) listEl.insertBefore(node, ref);
      prev = node;
    }
  }

  function renderDetail(article) {
    detailTitleEl.textContent = article.title || "(untitled)";

    detailMetaEl.replaceChildren();
    const dateText = formatAbsolute(article.published);
    if (dateText) {
      const dateNode = document.createElement("span");
      dateNode.textContent = dateText;
      detailMetaEl.appendChild(dateNode);
    }

    const body = article.content || article.summary;
    const type = article.content_type || "text/markdown";
    // Markdown -> HTML via marked; HTML feeds pass through as-is.
    // DOMPurify strips anything unsafe before it touches the DOM.
    const html = body
      ? type === "text/html"
        ? body
        : marked.parse(body)
      : "<p>(No content provided in the feed.)</p>";
    detailBodyEl.innerHTML = DOMPurify.sanitize(html);

    detailToggleBtn.textContent = article.read
      ? "Mark as unread"
      : "Mark as read";
  }

  function buildArticleNode(article) {
    const li = document.createElement("li");
    li.className = "article";
    li.dataset.id = article.id;
    li.setAttribute("role", "button");
    li.setAttribute("tabindex", "0");

    const dot = document.createElement("span");
    dot.className = "article-dot";
    dot.setAttribute("aria-hidden", "true");

    const body = document.createElement("div");
    body.className = "article-body";

    const title = document.createElement("h3");
    title.className = "article-title";

    const meta = document.createElement("div");
    meta.className = "article-meta";

    const description = document.createElement("p");
    description.className = "article-description";

    body.appendChild(title);
    body.appendChild(meta);
    body.appendChild(description);

    li.appendChild(dot);
    li.appendChild(body);

    li.addEventListener("click", () => selectArticle(article.id));

    updateArticleNode(li, article);
    return li;
  }

  function updateArticleNode(node, article) {
    node.classList.toggle("read", Boolean(article.read));
    node.setAttribute(
      "aria-label",
      `${article.title} — ${article.read ? "read" : "unread"}`
    );

    const title = node.querySelector(".article-title");
    if (title.textContent !== article.title) title.textContent = article.title;

    const meta = node.querySelector(".article-meta");
    meta.replaceChildren(
      document.createTextNode(formatRelative(article.published) || "Just now"),
      ...(article.read ? [sepNode(), textNode("read")] : [])
    );

    const description = node.querySelector(".article-description");
    const text = summaryToText(article.summary || "", article.summary_type);
    if (description.textContent !== text) description.textContent = text;
  }

  function sepNode() {
    const span = document.createElement("span");
    span.className = "article-meta-sep";
    span.textContent = "·";
    return span;
  }

  function textNode(s) {
    return document.createTextNode(s);
  }

  // Plain-text snippet for the card preview: render to HTML (Markdown via
  // marked, or the feed's own HTML) then strip every tag with DOMPurify,
  // leaving clean text.
  function summaryToText(raw, type) {
    const html = type === "text/html" ? String(raw) : marked.parse(String(raw));
    const text = DOMPurify.sanitize(html, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
    return text.replace(/\s+/g, " ").trim();
  }

  function formatRelative(timestampMs) {
    if (!timestampMs) return "";
    const diff = Date.now() - timestampMs;
    if (diff < 0) return "just now";
    const minutes = Math.round(diff / 60000);
    if (minutes < 1) return "just now";
    if (minutes < 60) return `${minutes} min ago`;
    const hours = Math.round(minutes / 60);
    if (hours < 24) return `${hours} hr ago`;
    const days = Math.round(hours / 24);
    if (days < 7) return `${days} day${days === 1 ? "" : "s"} ago`;
    return new Date(timestampMs).toLocaleDateString();
  }

  function formatAbsolute(timestampMs) {
    if (!timestampMs) return "";
    try {
      return new Date(timestampMs).toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      });
    } catch {
      return new Date(timestampMs).toString();
    }
  }

})();
