// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

(() => {
  const publishedEl = document.getElementById("published");
  const totalEl = document.getElementById("total");
  const listEl = document.getElementById("article-list");
  const resetBtn = document.getElementById("reset");
  const addBtn = document.getElementById("add");
  const removeBtn = document.getElementById("remove");

  function render(state) {
    publishedEl.textContent = state.published;
    totalEl.textContent = state.total;

    addBtn.disabled = state.published >= state.total;
    removeBtn.disabled = state.published <= 0;

    listEl.replaceChildren();
    if (state.titles.length === 0) {
      const empty = document.createElement("li");
      empty.className = "empty";
      empty.textContent = "Nothing published.";
      listEl.appendChild(empty);
      return;
    }
    for (const title of state.titles) {
      const li = document.createElement("li");
      li.textContent = title;
      listEl.appendChild(li);
    }
  }

  async function call(path, method) {
    const response = await fetch(path, { method });
    if (!response.ok) throw new Error(`${path} → HTTP ${response.status}`);
    render(await response.json());
  }

  resetBtn.addEventListener("click", () => call("/server/reset", "POST"));
  addBtn.addEventListener("click", () => call("/server/add", "POST"));
  removeBtn.addEventListener("click", () => call("/server/remove", "POST"));

  call("/server/state", "GET");
})();
