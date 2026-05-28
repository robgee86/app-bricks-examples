# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

import time
from calendar import timegm
from dataclasses import dataclass
from typing import Callable

import feedparser

from arduino.app_utils import brick, Logger


logger = Logger("rss-reader-brick")


@dataclass
class Article:
    id: str
    title: str
    summary: str
    summary_type: str
    content: str
    content_type: str
    published: int  # epoch milliseconds
    read: bool = False


@brick
class RSSReader:
    """
    Polls an RSS feed and notifies subscribers via two callbacks:
    `on_new_articles` (fires with just the newly-arrived entries) and
    `on_snapshot` (fires with the full sorted snapshot after every change).
    """

    def __init__(
        self,
        feed_url: str,
        poll_interval_seconds: int = 10,
        max_articles: int = 5,
    ):
        self._feed_url = feed_url
        self._poll_interval = poll_interval_seconds
        self._max = max_articles
        self._articles: dict[str, Article] = {}
        self._on_new: Callable[[list[Article]], None] | None = None
        self._on_snapshot: Callable[[list[Article]], None] | None = None

    def on_new_articles(self, cb: Callable[[list[Article]], None]):
        """
        Register a callback fired with the list of just-arrived articles
        every time the poll loop discovers any new entry.
        """
        self._on_new = cb

    def on_snapshot(self, cb: Callable[[list[Article]], None]):
        """
        Register a callback fired with the full sorted snapshot whenever
        the article set or any article's read state changes.
        """
        self._on_snapshot = cb

    def snapshot(self) -> list[Article]:
        """Return the current articles sorted newest-first."""
        return sorted(self._articles.values(), key=lambda a: a.published, reverse=True)

    def mark_read(self, aid: str, value: bool):
        """Flip an article's read flag; no-op if unchanged. Fires `on_snapshot`."""
        a = self._articles.get(aid)
        if a is None or a.read == value:
            return
        a.read = value
        self._fire_snapshot()

    @brick.loop
    def _poll(self):
        # feedparser.parse() sets bozo=1 on errors and leaves entries empty.
        parsed = feedparser.parse(self._feed_url)
        if parsed.bozo and not parsed.entries:
            logger.warning(f"Could not read feed: {parsed.bozo_exception!r}")
            time.sleep(self._poll_interval)
            return

        # Mirror the feed, keeping the entries we already know
        new_articles: dict[str, Article] = {}
        newly_arrived: list[Article] = []
        for entry in parsed.entries:
            aid = str(entry.id)
            if aid in self._articles:
                new_articles[aid] = self._articles[aid]
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
            a = Article(
                id=aid,
                title=str(entry.title),
                summary=str(summary),
                summary_type=str(summary_type),
                content=str(content),
                content_type=str(content_type),
                published=int(timegm(entry.published_parsed) * 1000),  # type: ignore[arg-type]
            )
            new_articles[aid] = a
            newly_arrived.append(a)

        while len(new_articles) > self._max:
            oldest = min(new_articles, key=lambda i: new_articles[i].published)
            del new_articles[oldest]

        self._articles = new_articles
        logger.info(f"{len(parsed.entries)} entries received, {len(self._articles)} stored")

        if newly_arrived and self._on_new:
            self._on_new(newly_arrived)
        self._fire_snapshot()
        time.sleep(self._poll_interval)

    def _fire_snapshot(self):
        if self._on_snapshot:
            self._on_snapshot(self.snapshot())
