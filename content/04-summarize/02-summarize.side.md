---
title: Give your summaries a personality
summary: The system prompt is the cheapest knob in your project — turn it.
---

The `system_prompt` we instantiate the `LargeLanguageModel` with is a single Python string. Changing it changes the voice, the format, the language, the length — without touching any other code.

The default we shipped is deliberately bland:

```
You are a news article summarizer. Respond with a few short markdown sentences. No preamble.
```

Try swapping it for something more opinionated. A few starting points:

- **A grumpy editor.**
  > You are a cranky veteran editor. Summarize the article in 2–3 short markdown sentences. Cut the hype, name the actual news, and end with a one-line take.
- **A scientist's eye.**
  > You are a curious scientist. Summarize the article in 2–3 short sentences and end with one open question worth investigating.
- **Bullet bullets bullets.**
  > Summarize the article as exactly 3 markdown bullets. No prose, no preamble.
- **Translate as you go.**
  > Summarize the article in 2–3 short Italian (or Spanish, or Japanese…) sentences. Respond in markdown. No preamble.
- **Pirate.** Because of course.
  > Ye be a pirate captain. Summarize this article in 2–3 short markdown sentences. Use light pirate-speak; do not be obnoxious about it.

Edit `prompt = ...` in `main.py`, restart the app, and refresh the page. Open an article you've never opened before (so the cache doesn't serve you the previous personality's summary) — and you'll see the new voice.
