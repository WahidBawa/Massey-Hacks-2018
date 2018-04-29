#include <Ultrasonic.h>
Ultrasonic s1(10,9);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int distCm = s1.distanceRead();
  Serial.println(distCm);
  delay(200);
}