# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from calendar import timegm

import feedparser

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App, Logger


FEED_URL = "http://192.168.1.5:7000/feed.xml"
MAX_ARTICLES = 5

logger = Logger("rss-reader")
logger.info(f"FEED_URL={FEED_URL}")

ui = WebUI()

articles: dict[str, dict] = {}


def fetch_feed():
    # feedparser.parse() sets bozo=1 on errors and leaves entries empty
    parsed = feedparser.parse(FEED_URL)
    if parsed.bozo and not parsed.entries:
        logger.warning(f"Could not read feed: {parsed.bozo_exception!r}")
        return

    global articles
    new_articles = {}
    for entry in parsed.entries:
        aid = str(entry.id)
        summary = entry.get("summary", "")
        summary_type = getattr(entry, "summary_detail", {}).get("type", "text/plain")
        if entry.get("content"):
            detail = entry.content[0]
            content = detail.get("value", "")
            content_type = detail.get("type", "text/html")
        else:
            content = summary
            content_type = summary_type
        new_articles[aid] = {
            "id": aid,
            "title": entry.title,
            "summary": summary,
            "summary_type": summary_type,
            "content": content,
            "content_type": content_type,
            "published": int(timegm(entry.published_parsed) * 1000),  # type: ignore[arg-type]
            "read": False,
        }
    while len(new_articles) > MAX_ARTICLES:
        oldest = min(new_articles, key=lambda i: new_articles[i]["published"])
        del new_articles[oldest]
    articles = new_articles

    # Display the fetched articles through the brick's logger.
    logger.info(f"Fetched {len(articles)} articles:")
    for article in articles.values():
        logger.info(f"  - {article['title']}")


def articles_payload():
    # Newest first — the UI renders them in this order.
    return sorted(articles.values(), key=lambda a: a["published"], reverse=True)


ui.expose_api("GET", "/articles", articles_payload)


@ui.app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https: data:; frame-ancestors 'none'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


fetch_feed()

App.run()
