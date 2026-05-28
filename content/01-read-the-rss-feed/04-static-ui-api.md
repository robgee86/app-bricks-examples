---
title: Show the articles in the UI
summary: Expose a REST endpoint and have the frontend fetch + render on load.
patches:
  - path: ../assets/1.4_static-ui-api.patch
    label: Expose /articles and fetch it from the page
    description: Adds a backend endpoint, security headers, and a `loadArticles()` call in app.js.
attachments:
  - path: ../assets/1.4_static-ui-api.zip
    label: rss-reader after step 1.4
---

Time to put articles on the screen.

We're going to do it the simple way first: expose a plain `GET /articles` REST endpoint that returns the list, and have the page call it once on load. No live updates yet — those come in milestone 2.

The patch changes both sides:

- **Backend** — `ui.expose_api("GET", "/articles", articles_payload)` registers a function that returns the articles sorted newest-first. We also slot in a small **security-headers middleware** now that the UI is actually serving content: a strict `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, etc. Boring, but the right time to add it.
- **Frontend** — `app.js` already has all the render machinery in place (that's what the starter shipped). All we add is a `loadArticles()` that calls `fetch("/articles")`, drops the result into `articles`, and re-renders.

Reload the page and you should see the cards appear in the feed panel. They're inert for now (clicking does nothing) — interactivity arrives in step 2.3.

> Try this: if the rss-server's director add or remove articles, hit refresh in the reader. The list updates on every reload because the page calls `/articles` on load. We'll make it live in the next milestone.

**Checkpoint:** the reader shows the same articles the rss-server is currently publishing.
