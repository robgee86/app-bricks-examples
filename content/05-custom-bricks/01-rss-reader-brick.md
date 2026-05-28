---
title: Wrap the feed logic in a custom brick
summary: Move feedparser + the poll loop + the article mirror into a reusable RSSReader brick.
patches:
  - path: ../assets/5.1_rss-reader-brick.patch
    label: Extract RSSReader into bricks/rss_reader/
    description: New `bricks/rss_reader/__init__.py` with a `@brick` class and a `@brick.loop` poll method; main.py slimmed and now subscribes to the brick's callbacks.
attachments:
  - path: ../assets/5.1_rss-reader-brick.zip
    label: rss-reader after step 5.1
---

`main.py` has been carrying feedparser, the poll loop, the mirror dict, and the read-state housekeeping for four milestones now. None of that is specific to this app — any RSS-driven app would do the same thing. That's exactly the shape that belongs in a brick.

## Custom bricks, in a nutshell

App Lab bricks aren't a privileged framework concept — `arduino:web_ui` and `arduino:llm` are just installed Python modules. You can write your own and keep them right next to your app. Three things make a brick a brick:

1. **A folder at `<app-root>/bricks/<name>/`** (sibling of `python/`) containing an `__init__.py` and a `brick_config.yaml`.
2. **The class is decorated with `@brick`** (from `arduino.app_utils`). That single decorator wires the instance into the AppController on construction — `start()` / `stop()` get called for you, threads get managed, etc.
3. **An entry in your app's `app.yaml`** referencing the brick by its `id` from `brick_config.yaml`, with no `arduino:` prefix:
   ```yaml
   bricks:
     - arduino:web_ui
     - arduino:llm: …
     - rss-reader:
   ```

The other key piece for our case is the **`@brick.loop` method decorator**. Slap it on a method and the framework calls it repeatedly on a dedicated thread — exactly what we were doing manually with `App.run(user_loop=poll_feed)`, except the brick now owns the cadence and you can have many of them in one app.

## What's in the brick

`bricks/rss_reader/__init__.py` defines two things:

- **`@dataclass Article`** — the typed shape of one entry (id, title, summary, content, published, read, …). No more passing opaque dicts around: callers consume real attributes (`a.title`, `a.read`) and the type checker has something to grip.
- **`@brick class RSSReader`** — constructor takes the feed URL plus optional `poll_interval_seconds` and `max_articles`. It owns a `_articles: dict[str, Article]` and a `@brick.loop` method `_poll` that:
  1. Parses the feed with the same bozo guard we already had.
  2. Mirrors the feed into a new dict, **preserving entries it already knows** (so `read` survives across polls).
  3. Evicts down to `max_articles`.
  4. Fires two callbacks: `on_new_articles(new)` with just the just-arrived entries, and `on_snapshot(snapshot)` with the full sorted list.
  5. Sleeps for the poll interval.

The brick also exposes `mark_read(id, value)` (which fires the snapshot callback on a real change) and a synchronous `snapshot()` accessor for code that needs the current list right now — useful when a brand-new websocket connects.

## What's in `main.py` now

A lot less. Gone:

- The `feedparser` / `timegm` / `time` imports.
- The `MAX_ARTICLES` / `POLL_INTERVAL_SECONDS` constants (now constructor arguments — defaults; pass them explicitly if you want to override). `FEED_URL` stays put and is passed straight into the `RSSReader(...)` call.
- The module-level `articles` dict.
- The entire `poll_feed` function.
- `App.run(user_loop=poll_feed)` → just `App.run()` (the brick's `@brick.loop` drives polling).

What's left is wiring: subscribe to the brick's two callbacks, broadcast snapshots over the WebUI, notify the sketch over the Bridge, prune the abstract cache, and route mark-read messages from the client into `reader.mark_read(...)`. `set_read` collapses from five lines to one. `make_abstract` looks up the article via `reader.snapshot()` instead of reaching into a global dict.

There's one boundary to remember: snapshots are `list[Article]` (dataclasses) inside Python, but the WebSocket needs JSON. The `broadcast_articles` helper uses `dataclasses.asdict` right at the WS boundary — that's the only place we go back to dicts.

> Side note on read-state. We chose to keep `read` **inside** the brick, on the `Article` itself. It's slightly less "purist" (read is arguably app-level state), but it keeps the diff small and matches what `mark_read` naturally controls. If you wanted a more decoupled brick, you'd drop `read` from the dataclass and track a sibling `dict[str, bool]` in your app.

**Checkpoint:** the reader behaves identically to the end of milestone 4 — live updates, mark-read, summaries, LED matrix on unread. The only visible difference is in your logs: every poll now also surfaces a `rss-reader-brick` line from the brick's own `Logger`, plus an `N new article(s): …` line from the consumer's `on_new_articles` callback when the rss-server's director adds an article.

🎉 You've built your first reusable brick. The two outro side quests in **◇ Bricks focus** point at obvious next moves — most notably a `Summarizer` brick that does for the LLM/cache plumbing what RSSReader did for the feed.
