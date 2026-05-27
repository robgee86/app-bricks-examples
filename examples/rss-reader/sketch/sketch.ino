// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>
#include <Arduino_LED_Matrix.h>
#include "frames.h"

Arduino_LED_Matrix matrix;

volatile int unread_count = 0;

void on_unread_count(int count) {
  unread_count = count;
  Serial.print("Unread articles: ");
  Serial.println(count);
}

void setup() {
  Serial.begin(9600);

  matrix.begin();
  matrix.clear();

  Bridge.begin();
  Bridge.provide("unread_count", on_unread_count);
}

void loop() {
  if (unread_count > 0) {
    matrix.loadFrame(unread_icon);
  } else {
    matrix.clear();
  }
  delay(300);
}
