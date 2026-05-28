---
title: Poll the feed in a loop
summary: Turn the one-shot fetch into a continuous user_loop.
patches:
  - path: ../assets/2.1_poll-loop.patch
    label: fetch_feed → poll_feed via App.run(user_loop=...)
attachments:
  - path: ../assets/2.1_poll-loop.zip
    label: rss-reader after step 2.1
---

A reader that fetches once at startup forces participants to restart the app every time the feed changes. Let's make it pull continuously.

App Lab's `App.run()` accepts a `user_loop=` callable. The framework calls it repeatedly on its own thread — you write what happens **once per tick** and the framework owns the scheduling. We rename `fetch_feed` to `poll_feed` and have it sleep `POLL_INTERVAL_SECONDS` (10 s by default) at the end of each iteration. The bozo branch also sleeps before returning, so a temporarily-unreachable feed doesn't spin the CPU.

Two small but important details land here:

- **Preserve known entries.** At the top of the entry loop, `if aid in articles: new_articles[aid] = articles[aid]; continue` reuses the existing dict for entries we already know. That keeps the per-entry `read` flag stable across polls — which matters as soon as we add the read feature in step 2.3.
- **One log line per poll.** The per-article info loop from step 1.3 collapses into a single summary: `{N} entries received, {M} stored`. Per-article spam on every poll gets old fast.

The UI hasn't changed — it still fetches `/articles` once at page load (from step 1.4). What changed is that the backend's `articles` dict now refreshes itself in the background. To **see** an update, the participant has to reload the page. That's exactly what step 2.2 fixes.

**Checkpoint:** add an article in the rss-server's director, wait up to 10 seconds, reload the reader. The new article is on the list.
