#include <RFID.h>

#include <SPI.h>

/*#include <deprecated.h>
#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <require_cpp11.h>*/

RFID monModuleRFID(10,9);
int UID[5];
int a=0;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  monModuleRFID.init();  
}

void loop() {
  if (monModuleRFID.isCard()) {  
          if (monModuleRFID.readCardSerial() and a==0) {        
            a=1;
            if (a==1) {
               Serial.print("Allumé.");
               delay(5000);
            }
          }          
          if (monModuleRFID.readCardSerial() and a==1) {
            a=0;
            if (a==0) {
              Serial.print("Éteint.");
              delay(5000);
            }
          }
    }
    delay(1); 
}
