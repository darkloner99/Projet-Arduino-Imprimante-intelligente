#include <RFID.h>

#include <SPI.h>



RFID monModuleRFID(10,9);
int UID[5];
int a=0;
int MASTERKEY[5]={2,121,37,217,135};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  monModuleRFID.init();  
}

void loop() {
  
  // Detect card 
  if (monModuleRFID.isCard()) { 
    Serial.println("Lecture.."); 
    
          // Get the id card
          if (monModuleRFID.readCardSerial() and a==0) {
            for(int i=0;i<=4;i++){
              UID[i]=monModuleRFID.serNum[i];
              Serial.print(UID[i],DEC);
            Serial.print("."); 
            }  
            
            // Check if the identifier is authorized
            if (UID[0] == MASTERKEY[0] && UID[1] == MASTERKEY[1] && UID[2] == MASTERKEY[2]
            && UID[3] == MASTERKEY[3] && UID[4] == MASTERKEY[4]) {   
              
              // Unlock the card    
              a=1;
              if (a==1) {
                 Serial.println("Allumé.");
                 delay(5000);
              }
               Serial.println("");
            } 
          }         
          // Get the id card
          else if (monModuleRFID.readCardSerial() and a==1) {
             for(int i=0;i<=4;i++){
              UID[i]=monModuleRFID.serNum[i];
              Serial.print(UID[i],DEC);
            Serial.print("."); 
            } 
            Serial.println("");
            // Check if the identifier is authorized
            if (UID[0] == MASTERKEY[0] && UID[1] == MASTERKEY[1] && UID[2] == MASTERKEY[2]
            && UID[3] == MASTERKEY[3] && UID[4] == MASTERKEY[4]) { 
            // Unlock the card       
            a=0;
            if (a==0) {
              Serial.println("Éteint.");
              delay(5000);
            }
          }
         }
    }
    delay(50); 
}
