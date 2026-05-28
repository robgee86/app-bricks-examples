---
title: Try a real RSS feed
summary: Point the reader at a public Atom/RSS feed instead of the demo server.
---

You don't have to stay on the demo server. `feedparser` understands both Atom and RSS 2.0, so pretty much any blog or news feed will work.

A few feeds that play nicely with this reader:

- `https://blog.arduino.cc/feed/` — Arduino blog
- `https://hnrss.org/frontpage` — Hacker News front page
- `https://lobste.rs/rss` — Lobsters
- `https://www.youtube.com/feeds/videos.xml?channel_id=<CHANNEL_ID>` — any YouTube channel

Change `FEED_URL` at the top of `main.py` and restart the app. You may want to bump `MAX_ARTICLES` while you're there — most public feeds publish many more items than the demo.

## Things you'll notice

- **Content types vary.** Some feeds give you Markdown content (like the demo server), most give you HTML, a few give you only a `summary`. The frontend already handles all three: it routes through `marked.parse` for Markdown, passes HTML through as-is, and falls back to the summary if there's no content. Sanitization happens with DOMPurify before anything reaches the DOM.
- **Dates can be wonky.** Some feeds publish without timezones, some lie. The "X min ago" label on each card uses `published_parsed`, which `feedparser` normalizes — but if a feed sets all dates to "now" the relative times will all collapse.
- **CSP may bite.** The security middleware sets `img-src 'self' https: data:`, so images served over HTTPS work but `http://`-only feeds may show broken images. Loosen the policy if you need to — but understand what you're trading.

## Going further

Try also:

- Aggregating **multiple feeds** by extending `fetch_feed()` to loop over a list of URLs and merge the results into `articles` before the `MAX_ARTICLES` eviction.
- Adding a **source** field per article (the feed's title) so cards can show where each article came from.
