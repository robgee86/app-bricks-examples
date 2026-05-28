---
title: Use the brick's Logger
summary: Replace print with arduino.app_utils.Logger.
patches:
  - path: ../assets/1.3_use-logger.patch
    label: Switch print → Logger
attachments:
  - path: ../assets/1.3_use-logger.zip
    label: rss-reader after step 1.3
---

`print` is fine for quick verification but it's not great for a longer-lived app — in the next step we'll use the brick's `Logger`, which gives us levels (info / warning / error) and a nicely tagged source.

App Lab ships one in `arduino.app_utils`. We create a single logger tagged with the app name (`"rss-reader"`) at module scope, then route everything through it:

- The bozo branch becomes `logger.warning(...)` — the right severity for "we couldn't read the feed".
- The "Fetched N articles" + per-title loop become `logger.info(...)`.
- We also log `FEED_URL` at startup, so it's obvious from the logs which feed the board is hitting (handy when the URL is wrong).

Log lines now carry the `rss-reader` tag and a level. They render in App Lab's Logs panel with severity coloring, which makes scanning a multi-app system much easier.

> Tip: the per-article info log is a workshop crutch — useful right now, but we'll collapse it into a single summary line once we move to a polling loop in milestone 2. Per-article spam on every poll gets noisy fast.

**Checkpoint:** logs show `INFO  rss-reader  FEED_URL=…` at startup and `INFO  rss-reader  Fetched N articles:` afterwards.
