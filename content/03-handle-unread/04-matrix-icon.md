---
title: Show an icon on the LED matrix
summary: Trade the single LED for a glyph on the on-board LED matrix.
patches:
  - path: ../assets/3.4_matrix-icon.patch
    label: Replace the LED blink with matrix.loadFrame()
    description: Adds Arduino_LED_Matrix, a placeholder icon in frames.h, and a matrix-based loop().
attachments:
  - path: ../assets/3.4_matrix-icon.zip
    label: rss-reader after step 3.4
---

A blinking dot is a signal; a change on the on-board LED matrix is way more communicative.

Three changes to the sketch:

- **Include the matrix library** — `#include <Arduino_LED_Matrix.h>` — and declare a global `Arduino_LED_Matrix matrix;`.
- **Initialize it** in `setup()` with `matrix.begin()` and `matrix.clear()`.
- **Pick the frame** in `loop()` — when `unread_count > 0`, draw an icon; otherwise clear the matrix.

The icon itself lives in a new **`frames.h`** sibling file. The patch ships a **placeholder** frame so the code compiles and runs out of the box. **It's intentionally generic — you'll want to design a real "you have mail" icon for your reader**: an envelope, a number, a letter — your call. The side quest below walks you through a friendly way to design one.

**Checkpoint:** the LED stops blinking; the matrix lights up with the placeholder icon shows up any time the unread count is non-zero.
