---
title: Design your own unread icon
summary: Use the LED Matrix Painter example to paint a glyph, then drop it into frames.h.
---

The frame the workshop ships is a placeholder. Designing one by hand in hex is painful — there's a much nicer way using the **LED Matrix Painter** example that ships with App Lab.

The Painter is a small App Lab app that exposes a clickable matrix in a web UI: you paint pixels, name the frame, and the app exports a `uint32_t[4]` constant you can paste straight into a `.h` file. Same encoding `matrix.loadFrame(...)` expects — drop it in and you're done.

## Steps

1. Open App Lab → **Examples** → **Led Matrix Painter**. Run it.
2. Open its web UI.
3. Draw your "unread mail" icon — an envelope, a closed eye, the letter **M**, a tiny mail-truck — whatever you like. The matrix gives you about 12×8 to play with.
4. Use the Painter's **Export** affordance to get the `const uint32_t name[4] = { 0x..., 0x..., 0x..., 0x... }` block.
5. Replace the contents of `examples/rss-reader/sketch/frames.h` with your new constant. Make sure the **identifier** matches what `sketch.ino` loads — by default that's `unread_icon`, so either rename your exported constant or update the `matrix.loadFrame(...)` call.
6. Re-flash the sketch and watch your glyph light up the next time the unread count is non-zero.

## Stretch

Why stop at one frame? A few directions:

- **Two frames, animated.** Have the icon "pulse" or "bob" — alternate two frames in `loop()` with a small delay. The Painter exports sequences too.
- **Per-count glyphs.** Read the integer `unread_count` and pick from an array of frames — show "1", "2", "3+" as separate icons.
- **A subtle "all read" pattern.** Instead of clearing the matrix when there's nothing unread, draw a faint dot or a checkmark.
