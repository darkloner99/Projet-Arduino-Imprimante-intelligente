#include <LiquidCrystal.h>

LiquidCrystal lcd(14,15,16,17,18,19);

void setup() {
  lcd.begin(16,2);
  lcd.clear();
  lcd.print("Coucou Apolline");
  lcd.setCursor(0,1);
  lcd.print("Tu es moche :)<");
}

void loop() {
  // put your main code here, to run repeatedly:

}
