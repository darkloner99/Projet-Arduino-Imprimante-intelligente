#include <SPI.h>
#include <RFID.h>

const char DOUT_LED_ROUGE = 2;
const char DOUT_LED_VERTE = 3;

RFID monModuleRFID(10,9);

int IUD[5]={};
int MASTERKEY[5]={2,121,37,217,135};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  monModuleRFID.init();
  pinMode(DOUT_LED_ROUGE, OUTPUT);
  pinMode(DOUT_LED_VERTE, OUTPUT);
  digitalWrite(DOUT_LED_ROUGE, LOW);
  digitalWrite(DOUT_LED_VERTE, LOW);

}

void loop() {
  if (monModuleRFID.isCard()) {
    Serial.print("L'UID est: ");
    for(int i=0;i<=4;i++);{
      UID[i]=monModuleRFID.serNum[i];
      Serial.print(UID[i],DEC);
      Serial.print(".");
    }
    Serial.println("");
  }

  if (UID[0] == MASTERKEY[0]

}
