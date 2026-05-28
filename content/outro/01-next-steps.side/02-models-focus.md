---
title: Models focus
summary: Chat about the article, swap models, navigate with gestures.
---

The LLM brick is the most generous "I'll change later" knob in this app. Three directions worth playing with:

## Add a chat for discussing the article

Right now the LLM only does one-shot summarization. Add a small chat panel under the article body where users can ask follow-up questions about what they're reading.

A reasonable shape:

- A new `arduino:llm` chat instance per article (or shared, with **memory enabled** this time — drop the `llm.with_memory(0)` for the chat). The cleanest separation is two LLM instances: `summarizer` (no memory) and `chat` (with memory).
- On the client, a small input box + message log inside the detail card. Each user message emits `chat_message` over the websocket; each model response comes back as `chat_reply`.
- Server-side, seed the chat with the article content so the model has context: `chat.chat(f"The article is:\n{content}\n\nQuestion: {user_question}")`.

`chat_stream` works really well here — tokens trickle in and the UI feels alive.

## Use a different model

`llamacpp:gemma-4-E2B-it-Q4_0_PURE` is a small, fast default. The bricks runtime supports several others; **genie-based** variants are particularly interesting because they're tuned for instruction-following.

Edit `model=` in the `LargeLanguageModel(...)` constructor and restart. Some axes to explore:

- **Smaller** for snappier latency on long articles, **larger** for richer summaries.
- **A model with a bigger native context** lets you drop the `[:6000]` truncation on `content`.
- **A multilingual model** if you're summarizing non-English feeds.

> Whichever you pick, do an apples-to-apples test on the same article — summary quality is the kind of thing that's only obvious side-by-side.

## Integrate the GestureRecognition brick to navigate articles

`arduino:gesture-recognition` reads the IMU (or a connected camera, depending on configuration) and emits high-level gestures: swipe-left, swipe-right, thumbs-up, etc. Wire those to article navigation:

- **swipe right** → mark current article read + open the next unread
- **swipe left** → previous article
- **thumbs-up** → mark all as read

The hook on the Python side is `gesture.on_event(lambda name: ...)`. From there it's the same `set_read` / `selectArticle` plumbing you already have — you just need to push a `selectArticle` message from the server to the client. (Or have the server send a `select_article` event the client routes through its existing `selectArticle()`.)

Hands-free RSS triage from your desk. Surprisingly satisfying.
