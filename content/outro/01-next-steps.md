---
title: Where to go from here
summary: A recap and three directions to keep exploring.
---

You did it. Your reader now:

- Polls an RSS feed on a background loop, with proper error handling and a `Logger` you can scan in App Lab's log panel.
- Pushes updates live to every connected browser over a websocket, with the server as the source of truth for both the article set and the read state.
- Talks to a sketch on the microcontroller over the **Bridge**, lighting an icon on the LED matrix whenever there are unread articles.
- Generates a short, cached summary for each article on demand, using a local LLM through the `arduino:llm` brick.
- Wraps the feed-polling logic into a **custom `RSSReader` brick** of your own — `@brick` + `@brick.loop`, with typed `Article` dataclasses crossing the API.

That's a complete little App Lab application end to end. The same shape — Python brick(s) + WebUI + a sketch on the MCU + an LLM — covers a wide range of projects you might want to build next.

## Three directions

Pick whichever side quest below pulls at you the most. Each one points at the next-most-useful brick or capability in App Lab.

- **◇ Bricks focus** — get more out of App Lab's stock bricks. Send notifications, persist state, package what you built into your own brick.
- **◇ Models focus** — extend the LLM half. Chat about the article, swap models, navigate hands-free.
- **◇ Sketch focus** — keep growing the hardware half. A modulino, more interactions on the MCU side.

And whichever you pick, please share what you build. We love seeing where these workshops end up — that's how the framework gets better.
