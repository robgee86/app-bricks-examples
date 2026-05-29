---
title: Talk to the sketch via the Bridge
summary: Python pushes the unread count to the sketch with Bridge.notify; the sketch receives it via Bridge.provide.
patches:
  - path: ../assets/3.2_bridge-notify.patch
    label: Bridge.notify on the Python side, Bridge.provide on the sketch side
attachments:
  - path: ../assets/3.2_bridge-notify.zip
    label: rss-reader after step 3.2
---

How does the Python talk to the sketch? Through the **Bridge** — a small RPC channel App Lab provides. Two flavors:

- **`Bridge.call(name, *args)`** — request-response. Use when you want a return value from the sketch.
- **`Bridge.notify(name, *args)`** — fire-and-forget. Use when you just want to push something.

We want the sketch to know the unread count any time it changes, with no return value — perfect fit for `notify`. The flow:

- **Python side.** Import `Bridge` from `arduino.app_utils`. Add a `notify_unread()` helper that computes `count = sum(1 for a in articles.values() if not a["read"])` and calls `Bridge.notify("unread_count", count)`. Call it wherever the unread count changes — that's at the end of `poll_feed()` (new articles, evictions) and at the end of `set_read()` (toggles).
- **Sketch side.** Include `<Arduino_RouterBridge.h>`, register a handler with `Bridge.provide("unread_count", on_unread_count)` after `Bridge.begin()`, and write the handler: `void on_unread_count(int count) { Serial.println(count); }`.

The sketch is just **logging** the count right now — that's deliberate. The point of this step is to prove the channel is open. Step 3.3 makes it light an LED; step 3.4 puts it on the matrix.

> Note: the parameter type on the sketch side has to match what Python sent. `Bridge.notify("unread_count", count)` with an `int` count maps to `void on_unread_count(int count)`. Mismatches will fail silently.

**Checkpoint:** open the MCU serial log. Open the reader, mark articles read/unread, watch new `Unread articles: N` lines appear with the right count.
