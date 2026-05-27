---
title: Arduino Core on Zephyr 0.55: Getting ready for the final mile
date: 2026-05-15
summary: Core 0.55 fixes Serial.println() without a bridge header, adds RTC and CAN Bus libraries, and supports Nicla Vision ahead of a June stable target.
---
![Arduino Core on Zephyr 0.55 release banner](https://blog.arduino.cc/wp-content/uploads/2026/05/Arduino.cc-Blogpost-Cover1100x600-1-1-1024x559.jpg)

We're releasing [version 0.55.0](https://github.com/arduino/ArduinoCore-zephyr/releases/tag/0.55.0) of the [Arduino® Core on Zephyr](https://blog.arduino.cc/2025/08/06/updated-arduino-cores-with-zephyros-beta/) today, and it's a meaningful one. This update resolves one of the most common friction points users have reported, adds support for two widely-used libraries, and brings us noticeably closer to our June target for marking this core stable and ending the BETA program. Concurrently, we'll begin deprecating the [corresponding cores based on mbedOS](https://blog.arduino.cc/2024/07/24/the-end-of-mbed-marks-a-new-beginning-for-arduino/).

If you've been following the beta, this one is worth updating to.

## Unified monitor and serial

The single most requested fix in this cycle was simple and reasonable: `Serial.println()` should just work.

On previous releases, users running the Arduino® UNO™ Q board had to be intentional about how they routed output — adding `#include <Arduino_RouterBridge.h>` and being mindful of target differences between IDE 2 and Arduino® App Lab. That friction is gone in 0.55.

We've reworked how outputs are routed and introduced a transparent alias, so printing to `Serial` or `Monitor` now delivers the expected result in both Arduino IDE 2 and Arduino App Lab. No bridge header required. If your existing sketch includes `Arduino_RouterBridge.h`, it'll still compile cleanly; it's just redundant now.

Print to your monitor without thinking about it.

## New library support

**Real-Time Clock (RTC)**: Projects running on Zephyr-supported boards can now use a reliable RTC to track time independently of uptime counters. Sync with a network time server, maintain a running clock with full calendar features, and build time-aware applications with confidence.

**CAN Bus**: The CAN library opens the door to automotive and industrial applications right from your UNO Q. Add a small CAN transceiver to your setup and you have everything you need to prototype automotive dashboards, robotics control systems, or any device network built on the CAN fieldbus standard.

## Also in the Zephyr 0.55 release

- Dynamic Interrupts for UNO Q
- shiftIn / shiftOut functions for serial data reading and writing on pins
- Zephyr workqueue support for managing low-priority interrupts
  - Fixes compilation of libraries that hard-require `wiring_private.h` and `pins_arduino.h`
  - Plenty of bug fixes: PWM, WiFi, and more

## Board support

Nicla Vision joins the supported lineup with this release.

The full compatibility list as of 0.55.0:

- UNO Q
- Arduino® Portenta™ H7
- Portenta C33
- Arduino® Opta™ board
- Arduino® Giga™ Display Shield
- Arduino® [Nano™ Matter](https://blog.arduino.cc/2026/03/10/your-arduino-nano-matter-board-is-now-a-professional-zephyr-development-platform/) board
- Nano 33 Bluetooth® LE
- Arduino® Nicla™ Sense board
- Nicla Vision

## How to get started

Search for "zephyr" in the Arduino IDE Board Manager, install the 0.55.0 release, and you're ready to go. Check our full release notes available on [GitHub](https://github.com/arduino/ArduinoCore-zephyr/releases/tag/0.55.0) and read our [troubleshooting article](https://support.arduino.cc/hc/en-us/articles/27251870677916-Migrating-to-Zephyr-core-0-55-0-on-UNO-Q) for more information.

## Contribute to the beta program!

This is your opportunity to shape the future of Arduino development! We welcome feedback, bug reports, and contributions to the core. Visit the [GitHub Issues page](https://github.com/arduino/ArduinoCore-zephyr/issues) to report bugs or suggest features. Your feedback will play a critical role in refining this integration and unlocking new possibilities for embedded systems.

Visit the [Arduino Core-Zephyr GitHub repository](https://github.com/arduino/ArduinoCore-zephyr) today and start exploring this exciting new platform! Thank you for being a part of the Arduino community.

*Arduino, UNO, Portenta, Opta, Giga, Nano, and Nicla and the Arduino logo are trademarks or registered trademarks of Arduino S.r.l.*
