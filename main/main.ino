const int r = 13;
const int g = 12;
const int b = 11;

void color(int r1, int g1, int b1) {
  analogWrite(r, r1);
  analogWrite(g, g1);
  analogWrite(b, b1);
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  int thing = analogRead(A2);
  if (30 < thing && thing < 100) {
    color(0,255,255);
  } else {
    color(0,255,0);
  }
  Serial.println(thing);
  delay(17);
}
