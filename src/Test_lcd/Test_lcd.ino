#include <LiquidCrystal.h>

LiquidCrystal lcd(2,3,4,5,6,7);

void setup() {
  lcd.begin(16,2);
  lcd.clear();
  lcd.print("Bonjour");
  lcd.setCursor(0,1);
  lcd.print("Je suis en Peip2");
}

void loop() {
  // put your main code here, to run repeatedly:

}
