const int Pas =3;
int Dir = 4;
int Dir2 = 5;

const int fast = 2    ;
int i= 0;

void setup() {
  Serial.begin(9600);
  pinMode(Pas,OUTPUT);
  pinMode(Dir,OUTPUT);
  pinMode(Dir2,OUTPUT);
  
}

void loop() {

  digitalWrite(Dir,LOW);
  digitalWrite(Dir2,HIGH);
  
  for(int x = 0; x < 600; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    i+=1;
    Serial.println(i);
    delay(fast);
    }
    i=0;
    
  digitalWrite(Dir,HIGH);
  digitalWrite(Dir2,LOW);
  
 for(int x = 0; x < 1200; x++) {
   digitalWrite(Pas, HIGH);
   delayMicroseconds(100);
    digitalWrite(Pas, LOW);
   delay(fast);
   }

  digitalWrite(Dir,LOW);
  digitalWrite(Dir2,HIGH);

  
   for(int x = 0; x < 1200; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    delay(fast);
    }
    i=0;
    
  digitalWrite(Dir,HIGH);
  digitalWrite(Dir2,LOW);
  
 for(int x = 0; x < 600; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    delay(fast);
    }

  //delay(0);
}
