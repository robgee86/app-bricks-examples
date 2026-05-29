---
title: Welcome
summary: What you'll build, what you'll learn, and how to set up.
attachments:
  - path: ../assets/0.2_initial-state.zip
    label: rss-reader starter
    description: A styled but empty rss-reader project — your starting point for milestone 1.
---

Over the next ~90 minutes you'll build a small but complete Arduino App Lab application that:

1. **Reads an RSS feed and displays the articles** in a web UI served by the `web_ui` brick.
2. **Receives new articles in real time** — first by polling, then by using a websockets.
3. **Handles unread articles on the microcontroller** — a sketch on the MCU reacts to the unread count, first with the built-in LED, then with the LED matrix.
4. **Summarizes articles on demand** using a local LLM through the `arduino:llm` brick.
5. **Wraps the RSS plumbing in a custom brick** of your own — same shape as the built-in ones, reusable across apps.

By the end you'll have touched five of the most useful primitives in App Lab — the `web_ui` brick, `App.run`'s user loop, the `Bridge` between Python and the sketch, the `LLM` brick, and the `@brick` / `@brick.loop` decorators for authoring your own — and you'll have a project you can keep playing with.

## How this handbook works

The workshop is a chain of small **steps**. Each step is one focused checkpoint — usually 5–15 minutes of work. Use the **← / →** keys to move between steps; the progress bar at the top tracks your position.

Every step ends with two things you can reach for:

- A **Code changes** section that shows the diff applied at that step. Each file has a one-click "Copy new code" button.
- An **Attachment** — the full project zipped at that step. If you fall behind or want to skip ahead, unzip it over your working folder and you're caught up.

Some steps have an optional **◇ Side quest** at the bottom — interesting detours that don't count toward progress. The **Outro** has three of them; pick whichever direction you want to keep exploring.

## Setup

If you don't have it already, please download the App Lab https://www.arduino.cc/en/software/#app-lab-section
