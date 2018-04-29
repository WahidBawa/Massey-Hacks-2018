const int r = 13;
const int g = 12;
const int b = 11;
bool shoot = false;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}

void loop() {
//  thing = map(thing, 800, 1023, 0, 2);
/*
  if (30 < thing && thing < 100) {
    color(0,255,255);
  } else {
    color(0,255,0);
  }
*/
  digitalWrite(2, HIGH);
  if (analogRead(A5) > 0)
    {
        shoot = true;
    }
  else
  {
    shoot = false;
  }  
  Serial.println(shoot);
  /*
  int thing = analogRead(A4);
  Serial.println(thing);
    delay(17);
    */
}


