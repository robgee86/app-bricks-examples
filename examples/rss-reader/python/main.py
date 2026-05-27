# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import time
from calendar import timegm

import feedparser

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App, Bridge, Logger


FEED_URL = "http://192.168.1.5:7000/feed.xml"
MAX_ARTICLES = 5
POLL_INTERVAL_SECONDS = 10

logger = Logger("rss-reader")
logger.info(f"FEED_URL={FEED_URL} poll_interval={POLL_INTERVAL_SECONDS}s")

ui = WebUI()

articles: dict[str, dict] = {}


def broadcast_articles(room: str | None = None):
    snapshot = sorted(articles.values(), key=lambda a: a["published"], reverse=True)
    ui.send_message("articles_update", {"articles": snapshot}, room=room)


def notify_unread():
    # Tell the sketch how many unread articles there are, over the Bridge.
    count = sum(1 for a in articles.values() if not a["read"])
    Bridge.notify("unread_count", count)


def poll_feed():
    # feedparser.parse() sets bozo=1 on errors and leaves entries empty
    parsed = feedparser.parse(FEED_URL)
    if parsed.bozo and not parsed.entries:
        logger.warning(f"Could not read feed: {parsed.bozo_exception!r}")
        time.sleep(POLL_INTERVAL_SECONDS)
        return

    # Mirror the feed, keeping the entries we already know.
    global articles
    new_articles = {}
    for entry in parsed.entries:
        aid = str(entry.id)
        if aid in articles:
            new_articles[aid] = articles[aid]
            continue

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

    logger.info(f"{len(parsed.entries)} entries received, {len(articles)} stored")
    broadcast_articles()
    notify_unread()

    time.sleep(POLL_INTERVAL_SECONDS)


def set_read(data, value: bool):
    article = articles.get(data["id"])
    if article is None or article["read"] == value:
        return
    article["read"] = value
    broadcast_articles()
    notify_unread()


ui.on_connect(lambda sid: broadcast_articles(room=sid))
ui.on_message("mark_read", lambda _sid, data: set_read(data, True))
ui.on_message("mark_unread", lambda _sid, data: set_read(data, False))


@ui.app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https: data:; frame-ancestors 'none'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


App.run(user_loop=poll_feed)
