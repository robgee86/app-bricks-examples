---
title: Fetch the feed once
summary: Pull the demo feed with feedparser, store the entries, handle errors.
patches:
  - path: ../assets/1.1_fetch-feed-once.patch
    label: Add the feedparser fetch
    description: Imports, a `MAX_ARTICLES` cap, a `fetch_feed()` function that uses the `FEED_URL` you set in the intro, one call at startup.
attachments:
  - path: ../assets/1.1_fetch-feed-once.zip
    label: rss-reader after step 1.1
    description: The full project at this checkpoint, in case you fall behind.
---

The starter project serves a styled but empty UI. Our first job is to actually go get the articles.

We'll use the `feedparser` library to fetch the feeds served by the rss-server, normalize each entry into a plain dict, and stash them in a module-level `articles` dictionary keyed by entry id. This first version runs **once at startup** — we'll turn it into a continuous poll in milestone 2.

A few things to notice in the patch:

- **`MAX_ARTICLES`** and **`FEED_URL`** (which you configured in the intro) are added at the top of the file. It caps the in-memory mirror so a runaway feed can't grow without bound.
- **`feedparser.parse()`** never throws. On a malformed feed or a network error it sets `parsed.bozo = 1` and leaves `parsed.entries` empty. We guard on that and `print` a warning — good enough for now; in step 1.3 this becomes a proper `logger.warning`.
- We **mirror only what we need** out of each entry: `id`, `title`, `summary` (+ its mime type), `content` (+ its mime type), an integer-ms `published` timestamp, and a `read: False` flag. Keeping the model small now will pay off across the next few steps.
- **`MAX_ARTICLES`** eviction at the end keeps the dict bounded by dropping the oldest entries.

Nothing is on screen yet — the UI still shows "Waiting for articles…". That's fine; we're wiring the data path first, then surfacing it in step 1.4.

**Checkpoint:** restart the app, look at the App Lab logs, and confirm no `Could not read feed` line. (If you see one, double-check `FEED_URL` — it must be reachable from the board, and the rss-server's director must have at least one article published.)
