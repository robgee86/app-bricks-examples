---
title: Bricks focus
summary: Notifications, persistence, and packaging — get more out of App Lab's stock bricks.
---

You used three bricks in the workshop — `web_ui`, `llm`, and your own `rss-reader`. App Lab ships several more, and writing your own is a first-class flow. Three nice extensions of the reader:

## Integrate the Telegram brick

Add `arduino:telegram` to `app.yaml` and have the app DM you whenever a new article arrives. The hook is already there — the `on_new_articles(new)` callback you wired in milestone 5 fires with exactly the articles that just landed. Inside it, send one Telegram message per article (title + link).

Things to think about:

- **Don't spam at startup.** On the very first poll, *every* article looks new. Either skip the first call, or only notify entries published after the app started.
- **Bot token + chat id** live in environment variables or settings — don't hard-code them. App Lab gives you a settings UI for this.

## Persist state with the SQLStore brick

Right now the `read` state lives inside the `RSSReader` brick's in-memory mirror, and the `abstracts` cache lives in `main.py`. Both vanish on restart. `arduino:sql-store` gives you a thin SQLite wrapper that fits this perfectly.

Two tables — `read_state(article_id, read_at)` and `abstracts(article_id, text, generated_at)` — and three small additions:

- On startup, hydrate `abstracts[...]` from the DB, and replay the saved `read` flags onto the `RSSReader` snapshot (via `reader.mark_read(id, True)` for each saved id).
- In `set_read()`, upsert into `read_state` alongside the call to `reader.mark_read(...)`.
- In `make_abstract()`, upsert into `abstracts` after a successful generation.

The `on_snapshot` callback that already prunes `abstracts` for evicted articles is also a good place to delete the matching DB rows.

## Create a custom brick for the Summarizer

The summarization logic in `main.py` is small but self-contained: a model, a system prompt, a `chat()` call, and a cache. That's a great shape for a reusable brick — exactly like you did for `RSSReader` in milestone 5.

A `summarizer` brick would expose something like:

```python
summarizer = Summarizer()                                     # bricks/summarizer/__init__.py
text = summarizer.summarize(article.content[:6000])           # encapsulates the LLM + prompt
```

Hide the model id, the context-size dance, and the system prompt behind a `@brick`-decorated class in `bricks/summarizer/__init__.py`. Add it to `app.yaml` next to `rss-reader:`. `main.py` becomes even slimmer — and the next App Lab project that needs to summarize anything can just import yours.

The interesting design question is **where the abstract cache lives**: inside the brick (Summarizer becomes opinionated about caching and how to invalidate) or outside (`main.py` keeps the dict it has today). Both are defensible; pick the one that makes the brick most reusable for *your* next app.
