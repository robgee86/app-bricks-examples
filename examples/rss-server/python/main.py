# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from fastapi import Response

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App, Logger

CHANNEL_TITLE = "Arduino Demo Feed"
CHANNEL_DESCRIPTION = "A handful of fake articles for the RSS reader example."
ARTICLES_DIR = Path(__file__).resolve().parent.parent / "assets" / "articles"
ATOM_NS = "http://www.w3.org/2005/Atom"

logger = Logger("rss-server")


def parse_date(value: str) -> datetime:
    # Accept "YYYY-MM-DD" or a full ISO timestamp; assume UTC if no timezone.
    # Fall back to "now" so a missing/invalid date never breaks the feed.
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return datetime.now(tz=timezone.utc)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_article(text: str) -> dict:
    # Minimal frontmatter: a leading `---` block of `key: value` lines, then
    # the body. `title`, `summary` and `date` come from the frontmatter; the
    # body is the full article content. If `summary` is omitted, the first
    # paragraph is used as a fallback.
    lines = text.splitlines()
    meta: dict[str, str] = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            key, _, value = lines[i].partition(":")
            meta[key.strip()] = value.strip()
    content = "\n".join(lines[body_start:]).strip()
    return {
        "title": meta.get("title", "(untitled)"),
        "summary": meta.get("summary") or content.split("\n\n", 1)[0].strip(),
        "date": parse_date(meta.get("date", "")),
        "content": content,
    }


def load_articles() -> list[dict]:
    # Ordered by frontmatter date, oldest first. The server reveals newer
    # articles as you "add", so each one surfaces at the top of the reader.
    articles = [parse_article(f.read_text(encoding="utf-8")) for f in ARTICLES_DIR.glob("*.md")]
    articles.sort(key=lambda a: a["date"])
    logger.info(f"Loaded {len(articles)} articles from {ARTICLES_DIR}")
    return articles


ALL_ARTICLES = load_articles()

# Server state: how many articles (from the top of the ordered list) are
# currently published in the feed. Starts at the first article only.
published_count = min(1, len(ALL_ARTICLES))


def make_guid(article: dict) -> str:
    payload = f"{article['title']}|{article['content']}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def build_feed() -> bytes:
    now = datetime.now(tz=timezone.utc)
    published = ALL_ARTICLES[:published_count]

    feed = Element("feed", {"xmlns": ATOM_NS})
    SubElement(feed, "title").text = CHANNEL_TITLE
    SubElement(feed, "subtitle").text = CHANNEL_DESCRIPTION
    SubElement(feed, "id").text = "urn:arduino:rss-demo"
    SubElement(feed, "updated").text = now.isoformat()

    # content type="text/markdown" tells feedparser to leave the body verbatim
    # (no HTML processing) and lets the reader know to render it as Markdown.
    for article in published:
        guid = make_guid(article)
        pub = article["date"].isoformat()
        entry = SubElement(feed, "entry")
        SubElement(entry, "title").text = article["title"]
        SubElement(entry, "id").text = f"urn:arduino:article:{guid}"
        SubElement(entry, "updated").text = pub
        SubElement(entry, "published").text = pub
        SubElement(entry, "summary", {"type": "text"}).text = article["summary"]
        SubElement(entry, "content", {"type": "text/markdown"}).text = article["content"]

    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(feed, encoding="utf-8")


def serve_feed():
    return Response(
        content=build_feed(),
        media_type="application/atom+xml",
        headers={"Cache-Control": "no-store"},
    )


def server_state() -> dict:
    return {
        "published": published_count,
        "total": len(ALL_ARTICLES),
        "titles": [a["title"] for a in ALL_ARTICLES[:published_count]],
    }


def server_reset() -> dict:
    global published_count
    published_count = min(1, len(ALL_ARTICLES))
    logger.info(f"Reset: publishing {published_count} article(s)")
    return server_state()


def server_add() -> dict:
    global published_count
    published_count = min(published_count + 1, len(ALL_ARTICLES))
    logger.info(f"Add: publishing {published_count} article(s)")
    return server_state()


def server_remove() -> dict:
    global published_count
    published_count = max(published_count - 1, 0)
    logger.info(f"Remove: publishing {published_count} article(s)")
    return server_state()


ui = WebUI()
ui.expose_api("GET", "/feed.xml", serve_feed)
ui.expose_api("GET", "/server/state", server_state)
ui.expose_api("POST", "/server/reset", server_reset)
ui.expose_api("POST", "/server/add", server_add)
ui.expose_api("POST", "/server/remove", server_remove)


@ui.app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    return response


App.run()
