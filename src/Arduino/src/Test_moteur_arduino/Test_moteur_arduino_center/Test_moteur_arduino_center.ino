
// Define IO
const int Pas =2;
const int Dir = 3;



const int fast = 1;
int i= 0;

void setup() {
  Serial.begin(9600);
  pinMode(Pas,OUTPUT);
  pinMode(Dir,OUTPUT);
  
}

void loop() {

  digitalWrite(Dir,LOW);
  for(int x = 0; x < 250; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    delay(fast);
    }
    i=0;
    
 digitalWrite(Dir,HIGH);
 for(int x = 0; x < 500; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    delay(fast);
    }

    
  digitalWrite(Dir,LOW);
  for(int x = 0; x < 250; x++) {
    digitalWrite(Pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(Pas, LOW);
    delay(fast);
    }
    i=0;
    

}
