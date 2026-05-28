---
title: Add a reload button
summary: A manual refresh button — for one step only, until websockets land.
patches:
  - path: ../assets/2.2_reload-button.patch
    label: A Reload button that refetches /articles
attachments:
  - path: ../assets/2.2_reload-button.zip
    label: rss-reader after step 2.2
---

Reloading the page to see new articles is annoying. Let's add a button that refetches in place.

This is a deliberately small step. We add one `<button id="reload-btn">` to the feed-panel header and one click handler in `app.js` that calls our existing `loadArticles()`. That's it — same REST endpoint, same render path.

It's worth seeing why this isn't the right end-state, though:

- The user still has to **click** to know there's something new.
- A click triggers a fresh `fetch("/articles")`, which throws away any local UI state (selected article, scroll position, future read state…) and rebuilds from scratch.
- And it tells you nothing about whether the connection is even alive.

Step 2.4 fixes all of these by switching to a **websocket** the backend pushes into — but that's a bigger change, and walking through "REST → reload → push" makes the moving parts visible. The reload button is transient: it shows up here and disappears in 2.4.

**Checkpoint:** click **Reload** and the list refreshes without a page reload.
