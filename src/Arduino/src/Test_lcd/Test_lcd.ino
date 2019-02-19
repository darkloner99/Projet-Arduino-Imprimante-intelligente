#include <LiquidCrystal.h>

LiquidCrystal lcd(14,15,16,17,18,19);

void setup() {
  lcd.clear();
  lcd.begin(16,2);

 
}

void loop() {
  // put your main code here, to run repeatedly:
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("En cours");
  lcd.setCursor(0,1);
  lcd.print("d'impression");
  delay(2000);
  lcd.clear();
 
  

}
