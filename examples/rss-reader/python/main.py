# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import asdict

from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.llm import LargeLanguageModel
from arduino.app_utils import App, Bridge, Logger

from bricks.rss_reader import Article, RSSReader


FEED_URL = "http://192.168.1.5:7000/feed.xml"

logger = Logger("rss-reader")

prompt = "You are a news article summarizer. Respond with a few short markdown sentences. No preamble."
llm = LargeLanguageModel(model="llamacpp:gemma-4-E2B-it-Q4_0_PURE", system_prompt=prompt)
llm.with_memory(0)

reader = RSSReader(FEED_URL)
ui = WebUI()

abstracts: dict[str, str] = {}  # article id -> cached LLM abstract


def broadcast_articles(snapshot: list[Article], room: str | None = None):
    ui.send_message("articles_update", {"articles": [asdict(a) for a in snapshot]}, room=room)


def notify_unread(snapshot: list[Article]):
    # Tell the sketch how many unread articles there are, over the Bridge.
    count = sum(1 for a in snapshot if not a.read)
    Bridge.notify("unread_count", count)


def on_snapshot(snapshot: list[Article]):
    broadcast_articles(snapshot)
    notify_unread(snapshot)
    # Drop cached abstracts for articles that left the feed.
    ids = {a.id for a in snapshot}
    for stale in [aid for aid in abstracts if aid not in ids]:
        del abstracts[stale]


def on_new_articles(new: list[Article]):
    titles = ", ".join(a.title for a in new)
    logger.info(f"{len(new)} new article(s): {titles}")


def set_read(data, value: bool):
    reader.mark_read(data["id"], value)


def make_abstract(sid, data):
    aid = (data or {}).get("id")
    if not aid:
        return
    article = next((a for a in reader.snapshot() if a.id == aid), None)
    if article is None:
        return
    text = abstracts.get(aid)
    if text is None:
        logger.info(f"Generating abstract for {aid}")
        try:
            text = llm.chat(article.content[:6000])
        except Exception as e:
            logger.error(f"Abstract generation failed for {aid}: {e}")
            ui.send_message("abstract", {"id": aid, "error": True}, room=sid)
            return
        abstracts[aid] = text
    ui.send_message("abstract", {"id": aid, "text": text}, room=sid)


reader.on_new_articles(on_new_articles)
reader.on_snapshot(on_snapshot)

ui.on_connect(lambda sid: broadcast_articles(reader.snapshot(), room=sid))
ui.on_message("mark_read", lambda _sid, data: set_read(data, True))
ui.on_message("mark_unread", lambda _sid, data: set_read(data, False))
ui.on_message("request_abstract", make_abstract)


@ui.app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https: data:; frame-ancestors 'none'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


App.run()
