// SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
//
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>

void on_unread_count(int count) {
  Serial.print("Unread articles: ");
  Serial.println(count);
}

void setup() {
  Serial.begin(9600);
  Serial.println("RSS reader sketch ready");
  Bridge.begin();
  Bridge.provide("unread_count", on_unread_count);
}

void loop() {
  delay(1000);
}
