---
title: Live updates with websockets
summary: Swap REST + reload for a server-pushed websocket. The server becomes authoritative over read state.
patches:
  - path: ../assets/2.4_websockets.patch
    label: Switch to websockets; remove the Reload button
    description: The server pushes "articles_update" messages; the client emits "mark_read" / "mark_unread" back. The REST endpoint goes away.
attachments:
  - path: ../assets/2.4_websockets.zip
    label: rss-reader after step 2.4
---

This is the big one for milestone 2. We replace the REST + reload mechanic with a live, two-way websocket channel — and that change makes the server the single source of truth for both the articles **and** the read state.

The `web_ui` brick gives us the websocket primitives directly. On the backend:

- `ui.send_message(name, payload, room=...)` pushes a message to a connected client (or all, if `room` is `None`).
- `ui.on_connect(fn)` runs when a client connects; we use it to send that one client the current snapshot.
- `ui.on_message(name, fn)` registers a server-side handler for messages emitted by the client.

We wire that into three functions: `broadcast_articles()` (sends the full sorted list as `articles_update`), `set_read(data, value)` (flips the server's `read` flag and rebroadcasts), and a one-liner per handler (`mark_read`, `mark_unread`).

On the client we drop the `fetch`/`loadArticles` plumbing and connect a socket.io client to the same origin. Three handlers — `connect`, `disconnect`, `reconnect_attempt` — drive a small status chip in the header so you can see when things go offline. `articles_update` replaces `articles` in place and re-renders. The mark actions become `socket.emit("mark_read", { id })`-style calls; the server round-trips back through `broadcast_articles`, which is what triggers the re-render.

One thing to call out about the client render: **we reconcile in place**. Instead of `replaceChildren` on every update, we walk the existing card nodes and patch them. That keeps each card's slide-in animation from re-firing on every poll, which was visually noisy.

Two pieces of UI come and go in this step:

- The **Reload button** disappears — pushes obsolete it.
- A **connection-status chip** ("Live" / "Reconnecting" / "Offline") shows up in the header now that there's a connection to talk about.

**Checkpoint:** open the reader in two browser tabs. In tab A, click an article. The unread count drops in **both** tabs (server is authoritative now). Add an article in the rss-server's director — both reader tabs receive it within ~10 seconds without anyone clicking anything.
