---
title: Add a sketch
summary: A minimal sketch that runs on the MCU alongside the Python app.
patches:
  - path: ../assets/3.1_add-sketch.patch
    label: Create sketch/ with a no-op sketch.ino + sketch.yaml
attachments:
  - path: ../assets/3.1_add-sketch.zip
    label: rss-reader after step 3.1
---

App Lab apps can have **two components**: a Python "MPU" (what we've been building) and a sketch "MCU" compiled to the microcontroller. They live in the same project, and App Lab handles building, flashing and running both.

The presence of a `sketch/` folder with a `sketch.yaml` is all it takes — there's no extra brick to add to `app.yaml`. We create:

- **`sketch/sketch.yaml`** — a tiny profile file pinning the target platform (`arduino:zephyr` for the UNO Q).
- **`sketch/sketch.ino`** — a no-op sketch right now: `Serial.begin(9600)` and an empty loop with a `delay(1000)` to keep things quiet. We'll fill it with real logic over the next three steps.

When you next run the app, watch the App Lab build logs — they should compile the sketch and flash it to the board. That alone is the win for this step; the sketch isn't doing anything visible yet.

**Checkpoint:** the app rebuilds without errors and the MCU log shows `RSS reader sketch ready` shortly after start.
