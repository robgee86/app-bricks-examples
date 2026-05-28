---
title: Blink the built-in LED
summary: Translate the unread count into a visible blink on LED_BUILTIN.
patches:
  - path: ../assets/3.3_blink-led.patch
    label: Store the count and act on it in loop()
attachments:
  - path: ../assets/3.3_blink-led.zip
    label: rss-reader after step 3.3
---

Logging the count was a sanity check; let's actually **act** on it. When there are unread articles, blink `LED_BUILTIN`; otherwise leave it off.

Two small changes to the sketch:

- A module-level `volatile int unread_count = 0;` becomes the shared piece of state. The `on_unread_count` handler stores the value (Bridge providers run on their own thread — `volatile` keeps `loop()` from caching a stale copy in a register).
- `loop()` reads `unread_count` and either blinks (`HIGH` / `LOW` with a small `delay`) or holds the pin `LOW`. Pure conditional code; the Bridge does the rest.

> Aside on the LED pin: `LED_BUILTIN` resolves to the board's onboard LED. Most Arduino cores configure the pin automatically as you write to it, which is why you don't see a `pinMode(LED_BUILTIN, OUTPUT)` here — but adding one is harmless and many cookbooks include it. Pick whichever style matches the rest of the codebase you're working in.

The Python half didn't change in this step. All the wiring is on the sketch side.

**Checkpoint:** start with all articles read → LED off. Open an unread article in the reader, then go back, then mark it unread again → the LED blinks until the count hits zero again.
