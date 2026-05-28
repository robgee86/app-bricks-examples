---
title: Mark articles as read
summary: Detail view, an unread chip, a "mark all" button — entirely client-side for now.
patches:
  - path: ../assets/2.3_mark-read.patch
    label: Detail view + read/unread state
    description: Adds the unread chip, the "Mark all as read" button, the click-to-open behaviour, and the toggle inside the detail view.
attachments:
  - path: ../assets/2.3_mark-read.zip
    label: rss-reader after step 2.3
---

So far the cards are inert. Let's give the reader an actual reader experience: tap a card → open the article in a detail view → mark-as-read on open, with a toggle to undo.

All the read-state work in this step is **client-side** — we just flip a `read` boolean on the article object in `articles[]` and re-render. That's enough for a single browser session; making it persist across reloads and across multiple clients is what we'll wire up in step 2.4 (when the server becomes authoritative over read state).

The patch touches a few things:

- **`index.html`** gets an unread chip in the header and a "Mark all as read" button next to the existing Reload button.
- **`app.js`** picks up the corresponding refs and a small block of event listeners — `markAllBtn`, `backBtn`, `detailToggleBtn`, plus a `selectArticle(id)` function the card click invokes. Each handler mutates `article.read` and calls `render()`. The `render()` function gains an unread-count block that drives the chip and the disabled state of "Mark all".

A couple of behavioral notes:

- **Mark on open.** Clicking a card opens its detail view *and* sets `read = true`. The dot on the card switches from teal (unread) to muted, and the unread chip ticks down.
- **The reload button still works** — but clicking it refetches `/articles`, which returns `read: False` for everything, wiping your local read state. That's a known limitation of "client-side only" read; we'll fix it next step.

**Checkpoint:** click a card → it opens, the unread count drops by one, the dot goes muted. Click **Back to articles**, then **Mark all as read** — the chip reads `0 unread`. Click **Reload** and watch the read state evaporate. (It's coming back, server-side, in step 2.4.)
