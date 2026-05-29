---
title: Sketch focus
summary: A modulino three-button controller for navigating the reader.
---

The sketch currently only **listens**. Let's give it a way to **talk back**.

## Modulino Buttons for navigation

Modulino Buttons is a small breakout with three capacitive buttons in a row. Wire it to the I²C connector and you can drive the reader with hardware:

- **Left** → previous article
- **Center** → jump to the latest unread
- **Right** → next article

The plumbing is symmetric to milestone 3, but in the opposite direction — sketch → Python instead of Python → sketch.

On the sketch side:

```cpp
#include <Arduino_Modulino.h>
ModulinoButtons buttons;

void setup() {
  Modulino.begin();
  buttons.begin();
  Bridge.begin();
  // ...
}

void loop() {
  if (buttons.update()) {
    if (buttons.isPressed(0)) Bridge.notify("nav", "prev");
    else if (buttons.isPressed(1)) Bridge.notify("nav", "latest");
    else if (buttons.isPressed(2)) Bridge.notify("nav", "next");
  }
}
```

On the Python side, register a provider and push the new selection over the websocket:

```python
def on_nav(direction):
    # Compute the new selected article from `articles` + the current state.
    # Then tell every connected client to select it.
    ui.send_message("select_article", {"id": chosen_id})

Bridge.provide("nav", on_nav)
```

The client adds a tiny `socket.on("select_article", ...)` handler that calls the existing `selectArticle(id)`. From the user's point of view, the same flow as clicking — just driven by buttons.

## Stretch

- **Long-press semantics.** `buttons.isPressed()` plus a small timer gives you "press" vs "long-press" — long-press center could mean "mark all as read".
- **A haptic chirp** on each press, so it feels alive — Modulino Buzzer pairs naturally.
- **Battery + headless mode.** Once buttons drive everything, the screen becomes optional. Run the app with no UI tab open and use the LED-matrix icon as your only feedback channel.
