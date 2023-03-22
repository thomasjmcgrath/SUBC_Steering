#include <Arduino.h>
const int analogPins[] = {A0, A1, A2, A3};

void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 4; i++) {
    int value = analogRead(analogPins[i]);
    Serial.print(value);

    if (i < 3) {
      Serial.print(" ");
    } else {
      Serial.println();
    }
  }
  delay(100); // Adjust this value to control the sampling rate
}