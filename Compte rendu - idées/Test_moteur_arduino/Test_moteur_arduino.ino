const int Pas =3;
const int Dir = 2;
void setup() {
  Serial.begin(115200);
  pinMode(Pas,OUTPUT);
  pinMode(Dir,OUTPUT);
  digitalWrite(Dir,HIGH);
}

void loop() {
  for(int x = 0; x < 200; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(1);
    digitalWrite(Pas, LOW);
    delay(1);
    }
  delay(0);
}
