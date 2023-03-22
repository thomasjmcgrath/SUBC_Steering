#include <Arduino.h>
int ap0 = A0; // UP
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int ap0val = analogRead(ap0);
  Serial.println(ap0val);
  delay(100);
 
}