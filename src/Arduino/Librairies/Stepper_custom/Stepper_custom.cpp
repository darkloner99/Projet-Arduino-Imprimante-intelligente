
#include "Arduino.h"
#include "Stepper_custom.h"

Stepper_custom::Stepper_custom(int DIR, int PAS)
{
    pinMode(DIR,OUTPUT);
    pinMode(PAS,OUTPUT);
    _dir = DIR;
    _pas = PAS;
    _speed = 10;
}

void Stepper_custom::onestep(int direction)
{
    if(direction>0){
        digitalWrite(_dir,HIGH);
    }else{
        digitalWrite(_dir,LOW);
    }

    digitalWrite(_pas, HIGH);
    delayMicroseconds(100);
    digitalWrite(_pas, LOW);
    delay(_speed);
}


void Stepper_custom::setspeed(int speed)
{
    _speed = speed;
}

void Stepper_custom::steps(int direction, int steps)
{
    for(int x = 0 ; x < steps; x++)
    {
        onestep(direction);
    }
}