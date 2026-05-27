// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>

volatile int unread_count = 0;

void on_unread_count(int count) {
  unread_count = count;
  Serial.print("Unread articles: ");
  Serial.println(count);
}

void setup() {
  Serial.begin(9600);
  Bridge.begin();
  Bridge.provide("unread_count", on_unread_count);
}

void loop() {
  if (unread_count > 0) {
    // Blink while there are unread articles.
    digitalWrite(LED_BUILTIN, HIGH);
    delay(300);
    digitalWrite(LED_BUILTIN, LOW);
    delay(300);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
    delay(300);
  }
}
