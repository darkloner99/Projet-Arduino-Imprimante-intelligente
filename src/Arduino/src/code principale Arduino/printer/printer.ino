#include <Stepper_custom.h>
#include <RFID.h>
#include <SPI.h>
#include <LiquidCrystal.h>
#include <stdio.h>
#include <math.h>

/*
* Ce code, chargé dans une carte arduino relié correctement à des moteurs permet d'imprimer
* une image envoyé en format gcode 
*/

// Motor 1 and 2 pin  
// Axe X
const int Pas_1_2 = 2;
const int Dir_1 = 3;
const int Dir_2 = 4;

// Motor 3 pin
// Axe Y
const int Pas_3 = 5;
const int Dir_3 = 6;

// Motor 4 pin
// Axe Z
const int Pas_4 = 7;
const int Dir_4 = 8;

// Enable
/*
 * A modififier !!!!! 
 * Les 19 ports étant utilisé sur ma carte arduino, j'an ai mis un au hassard
 * veuilez mettre un vrai port pour toute utilisation
 * Si enable est mis su HIGh, tout les moteurs sont stopé 
 */
const int ENABLE = 25;

// Initialise Stepper Motor
Stepper_custom StepperX(Dir_1, Pas_1_2);
Stepper_custom StepperX_2(Dir_2, Pas_1_2);
Stepper_custom StepperY(Dir_3, Pas_3);
Stepper_custom StepperZ(Dir_4, Pas_4);

// Motor info and variable
int MicroStep = 8;
float AnglePerStep = 1.8;
float Circumference = 31.4;
float NbStepPerRotation = 360 / AnglePerStep;
float StepsPerMillimeter = (NbStepPerRotation / Circumference) * MicroStep;
float StepInc = -1;
int StepDelay = 0;
int LineDelay = 0;
int penDelay = 50;

// Position Variable
 
float Xpos = 0;
float Ypos = 0;
int Zpos = 1;
float Xmax = 200;
float Ymax = 300;
float Xmin = 0;
float Ymin = 0;

double newPosX;
double newPosY;
double newPosZ;
double cx;
double cy;
double dir;
double CM_PER_SEGMENT = 1;

// RFID

RFID monModuleRFID(10,9);
int locker = 0;
int UID[5];
int MASTERKEY[5]={2,121,37,217,135};

// LCD

LiquidCrystal lcd(14,15,16,17,18,19);
char msg[16];

// global variables

int speedMotor;

int WORD_INDEX = 0;
int CHARAC_INDEX = 0;
int LINE_INDEX;
int LINE_COMMAND_LENGH;
boolean line = false;
boolean arc  = false;

#define TAB1LENGHT 10
#define TAB1LARGER 15

char subChain[TAB1LENGHT][TAB1LARGER];
boolean verbose = false;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  //pinMode(ENABLE, OUTPUT);
  pinMode(Pas_1_2, OUTPUT);
  pinMode(Pas_3, OUTPUT);
  pinMode(Pas_4, OUTPUT);

  pinMode(Dir_1, OUTPUT);
  pinMode(Dir_2, OUTPUT);
  pinMode(Dir_3, OUTPUT);
  pinMode(Dir_4, OUTPUT);

  StepperX_2.setspeed(1);
  StepperX.setspeed(1);
  StepperY.setspeed(1);
  StepperZ.setspeed(1);


  SPI.begin();
  monModuleRFID.init();  

  lcd.clear();
  lcd.begin(16,2);

}

void loop()
/*
 * Main Loop Here !!!
 * Delay allows to arduino to not bug
*/
{
  if (readRFID())
  {
    // locker = 0 ou 1 si activé ou non
    locker = changeLockerState(locker);
    //Serial.print("Locker changed state :");
    //Serial.println(locker);
    if (locker == 1) printCompiledMessage(2);
    delay(1500);
  }
  if (locker == 0) // locker ==1
  {
    if (Serial.available())
    {
      // on récupere la commande (tableau de 10*15 char)
      char *commandLine = getCommandLine();
      // on l'envoie à execCommandLine qui l'interprete et l'execute
      execCommandLine(commandLine);
      
      // We return a validation message
      Serial.println("OK");
    }
    delay(1500);
  }
  else
  {
    // Print on LCD: Identification requise:
    printCompiledMessage(1);
  }
  delay(20);
}

//   ###################
//   # Utils functions #
//   ###################

void deleteSubchain()
// Reset Subchain
{

  char reset[10] = "          ";
  int i = 0;
  while (i < TAB1LENGHT)
  {

    strcpy(subChain[i], reset);
    i += 1;
  }
}

double extractDouble(char *ptr, int START, int END)
/*
*Extrait un double dans un tableau de char donné sous forme d'un pointeur
*/
{

  char number[15];
  int i = START;
  while (i < END)
  {

    number[i - START] = *(ptr + i);
    i += 1;
  }
  double n = atof(number);
  return n;
}

char *getArrayElement(char *ptr, int index)
// Retourne l'élement d'un tableau de char
{

  return &(*(ptr + index * TAB1LARGER));
}

void newPrintSerial(char *ptr)
// Permet d'afficher un tableau donné sous forme d'un pointeur
{

  int i = 0;
  while (i < TAB1LARGER)
  {

    Serial.print(*(ptr + i));
    i += 1;
    if (*(ptr + i) == '\0')
    {
      break;
    }
  }
  Serial.println("");
}

char getNextCharac(char *ptr)
// récupere la prochaine char de notre variable word_c (sous ensemble de subchain)
{

  CHARAC_INDEX += 1;
  return *(ptr + CHARAC_INDEX - 1);
}

char *getNextWord(char *ptr)
// recupere le prochain mot de subchain(tableaux de 10 mots de max 15 charactères)
{

  char *ptr_2 = getArrayElement(ptr, WORD_INDEX);
  WORD_INDEX += 1;
  CHARAC_INDEX = 0;
  return ptr_2;
}

boolean checkIfNumber(char c)
{

  switch (c)
  {
  case '0':
    return true;
  case '1':
    return true;
  case '2':
    return true;
  case '3':
    return true;
  case '4':
    return true;
  case '5':
    return true;
  case '6':
    return true;
  case '7':
    return true;
  case '8':
    return true;
  case '9':
    return true;
  default:
    return false;
  }
}

char *splitLineInstruction(char str[])
// récupere dans le serial les instructions en les splitant en mots tous les A rencontrés
{

  int i = 0;
  int n = 0;
  char tmpSubChain[100];
  int tmpSubChain_index = 0;

  while (i < strlen(str))
  {
    char c = str[i];
    // tant qu'on a pas de A on récupere le prochain charactere
    if ('A' != c)
    {
      tmpSubChain[tmpSubChain_index] = c;
      tmpSubChain_index += 1;
    }
    else
    {
      // sinon on ajoute le mot a subchain 
      tmpSubChain[tmpSubChain_index] = '\0';
      tmpSubChain_index = 0;
      strcpy(subChain[n], tmpSubChain);
      memset(tmpSubChain, 0, sizeof(tmpSubChain));
      n += 1;
    }
    i += 1;
  }
  LINE_COMMAND_LENGH = n + 1;
  char *ptr = &subChain[0][0];
  return ptr;
}

// returns angle of dy/dx as a value from 0...2PI 
float atan3(float dy,float dx) 
{   
  float a=atan2(dy,dx);   
  if(a<0) a=(PI*2.0)+a;   
  return a; 
}

//  ##################################
//  # Serial and Bluetooth functions #
//  ##################################

char *getCommandLine()
{
  /*
  * Tant que le serial est disponible on récupere les charactéres envoyés
  * et ensuite on les envoies a splitLineInstruction
  */

  char str[100];
  char c;
  int index = 0;
  WORD_INDEX = 0;

  c = Serial.read();
  str[index] = c;
  index += 1;

  while (Serial.available())
  {
    c = Serial.read();
    str[index] = c;
    index += 1;
  }
  str[index] = '\0';
  char *ptr = splitLineInstruction(str);
  return ptr;
}

void execCommandLine(char *commandLine)
{
  /*
  * Lit commandLine qui est générer par splitLineInstruction et qui est un tableau de 
  * l'ensemble des mots (ou commande) envoyé a travers le serial et les interprete
  * 
  * Les commandes sont sous la forme :
  * G02AX20AY10A ...
  * ou encore:
  * E0
  */

  int WORD_INDEX = 0;
  int CHARAC_INDEX = 0;
  char BUFFER_1;
  char BUFFER_2;
  char BUFFER_3;
  char BUFFER_4;
  char *word_c = getNextWord(commandLine);

  delay(100);
  BUFFER_1 = getNextCharac(word_c);
  BUFFER_2 = getNextCharac(word_c);
  switch (BUFFER_1)
  {

  case 'G':

    if (BUFFER_2 == '0' or BUFFER_2 == '1' or BUFFER_2 == '2' or BUFFER_2 == '3' and checkIfNumber(BUFFER_2))
    {
      int i = 0;


      // G02 et G03 differents de G01 et G02
      if( BUFFER_2 == '2')
       {
        dir = 1;
       }
       if(BUFFER_2 == '3')
       {
        dir = -1;
       }


      // On lit tout les mots situé danns commandLIne grace a la fonction getNextWord
      while (i < TAB1LARGER)
      {

        word_c = getNextWord(commandLine);
        BUFFER_1 = getNextCharac(word_c);
        BUFFER_2 = getNextCharac(word_c);
        if (BUFFER_1 == 'X')
        {
          Serial.println("OKAY_X");
          newPosX = extractDouble(word_c, 1, 13);
        }
        else if (BUFFER_1 == 'Y')
        {
          Serial.println("OKAY_Y");
          newPosY = extractDouble(word_c, 1, 13);
        }
        else if (BUFFER_1 == 'F')
        {
          Serial.println("OKAY_F");
          if (BUFFER_2 == '1')
          {
            penDown();
          }
        }
        else if (BUFFER_1 == 'Z')
        {
          Serial.println("OKAY_Z");
          if (BUFFER_2 == '5')
          {
            penUp();
          }
        }
        else if (BUFFER_1 == 'I')
        {
          Serial.println("OKAY_I");
          arc = true;
          //line = false;
          cx = extractDouble(word_c, 1, 13);
        }
        else if (BUFFER_1 == 'J')
        {
          Serial.println("OKAY_J");
          arc = true;
          //line = false;
          cy = extractDouble(word_c, 1, 13);
          
        }

        i += 1;
      }
    }
    // G02 ou G03 = arc
    // G01 ou G00 = ligne
    if(arc)
      {
      Serial.print("arc:");
      Serial.print(arc);
      Serial.println("  drawing arc...");
      Serial.println(newPosX);
      Serial.println(newPosY);
      Serial.println(cx);
      Serial.println(cy);
      arc2(newPosX,newPosY,cx,cy,dir);
      arc = false;
      delay(50);
      }
      else
      {
      Serial.print("arc:");
      Serial.print(arc);
      Serial.println("  drawing line...");
      Serial.println(newPosX);
      Serial.println(newPosY);
      drawLine(newPosX, newPosY);
      arc = false;
      }
    deleteSubchain();
    break;

   


    

  case 'E':
   // Enable or not the drivers
    if (BUFFER_2 == '0')
    {
      digitalWrite(ENABLE, HIGH);
    }
    if (BUFFER_2 == '1')
    {
      digitalWrite(ENABLE, LOW);
    }
    break;

  case 'P':

   // We have already BUFFER_1 and BUFFER_2 so we get only
   // BUFFER_3
    BUFFER_3 = getNextCharac(word_c);
    BUFFER_4 = getNextCharac(word_c);
    // The next word is the word to print
    word_c = getNextWord(word_c);

    // Call printLCD to print it 
    printLCD(word_c ,BUFFER_1, BUFFER_2, BUFFER_3, BUFFER_4);

 

  default:

    //Serial.println(word_c);
    int i = 0;
    while (i < LINE_COMMAND_LENGH)
    {

      word_c = getNextWord(commandLine);
      //Serial.println(word_c);
      i += 1;
    }
    break;
  }

  deleteSubchain();
}

//   #########################
//   # Motor basic functions #
//   #########################

/*********************************
 * Draw a line from (x0;y0) to (x1;y1).
 **********************************/
void drawLine(float x1, float y1)
{

  //  Bring instructions within limits
  if (x1 >= Xmax)
  {
    x1 = Xmax;
  }
  if (x1 <= Xmin)
  {
    x1 = Xmin;
  }
  if (y1 >= Ymax)
  {
    y1 = Ymax;
  }
  if (y1 <= Ymin)
  {
    y1 = Ymin;
  }

  //  Convert coordinates to steps
  x1 = (x1 * StepsPerMillimeter);
  //Serial.println(x1);
  y1 = (y1 * StepsPerMillimeter);
  //Serial.println(y1);
  float x0 = (Xpos * StepsPerMillimeter);
  float y0 = (Ypos * StepsPerMillimeter);
  delay(10);

  //  Let's find out the change for the coordinates
  long dx = abs((x1 - x0));
  long dy = abs(y1 - y0);
  int sx = x0 < x1 ? StepInc : -StepInc;
  int sy = y0 < y1 ? StepInc : -StepInc;

  long i;
  long over = 0;

  if(false)
  {
  Serial.print("dx, dy :");
  Serial.print(dx);
  Serial.print(" ");
  Serial.println(dy);
  }
  
  // Go to coordinates 
  // over est en quelque sort la pente,
  // par exemple quand on avance de 3 on monte de 1
  if (dx > dy)
  {
    for (i = 0; i < dx; ++i)
    {
      StepperX.onestep(-sx);
      StepperX_2.onestep(sx);
      over += dy;
      if (over >= dx)
      {
        over -= dx;
        StepperY.onestep(sy);
      }
    }
  }
  else
  {
    for (i = 0; i < dy; ++i)
    {
      StepperY.onestep(sy);
      over += dx;
      if (over >= dy)
      {
        over -= dy;
        StepperX.onestep(-sx);
        StepperX_2.onestep(sx);
      }
    }
  }

  //  Delay before any next lines are submitted
  delay(10);
  //  Update the positions
  Xpos = (x1 / StepsPerMillimeter);
  ;
  Ypos = (y1 / StepsPerMillimeter);
  if (false)
  {
    Serial.print("X,Y :");
    Serial.print(Xpos);
    Serial.print(" ");
    Serial.println(Ypos);
  }
}


/*************************************************************
 * Draw a circle from (x0;y0) to (x1;y1).
 * cx,cy center coordinates circle 
 * 
 * Thanks to @Dan (Miscellaneous) for the solution
 * ***********************************************************
 * Attention: Fonction pas encore vérifié, il ne peut qu'elle
 * ne fonctionne pas
 *************************************************************/
void arc2(float x, float y, float cx, float cy, float dir)
{
  // get raduis
  float dx = Xpos - cx;
  float dy = Ypos - cy;
  float radius = sqrt(dx * dx + dy * dy);

  // find the sweep of the arc
  float angle1 = atan3(dy, dx);
  float angle2 = atan3(y - cy, x - cx);
  float sweep = angle2 - angle1;

  if (dir > 0 && sweep < 0)
    angle2 += 2 * PI;
  else if (dir < 0)
    angle1 += 2 * PI;

  sweep = angle2 - angle1;

  // get length of arc
  // float circumference=PI*2.0*radius;
  // float len=sweep*circumference/(PI*2.0);
  // simplifies to
  float len = abs(sweep) * radius;
  int i, num_segments = floor(len / CM_PER_SEGMENT);
  // declare variables outside of loops because compilers can be really dumb andinefficient some times.
  float nx, ny, nz, angle3, fraction;

  for (i = 0; num_segments < 1; ++i) 
  {
    // interpolate around the arc
    fraction = ((float)i) / ((float)num_segments);
    angle3 = (sweep * fraction) + angle1;

    // find the intermediate position
    nx = cx + cos(angle3) * radius;
    ny = cy + sin(angle3) * radius;
    // make a line to that intermediate position
    drawLine(nx, ny);
    delay(100);
  }
  // one last line hit the end
  drawLine(nx, ny);
}

void moveZ()
{

  if (Zpos == 0)
  {
    penUp();
    Zpos = 1;
  }
  else
  {
    penDown();
    Zpos = 0;
  }
}

void penUp()
/*
* Monte le stylo 
*/
{
  StepperZ.steps(-1, 140);
  Serial.println("penup");
}

void penDown()
/*
* Descent le stylo 
*/
{
  StepperZ.steps(1, 90);
  Serial.println("pendown");
}




//  ##################################
//  #         LCD Functions          #
//  ##################################

void printLCD(char *msg, int cursor ,int clear, int delay_1 ,int delay_2 )
/*
 * cursor set to 0 to top line and 1 top bottom line
 * clear set to 1 to reset screen
 * delay_1 correspond delay time between characters's printing
 * delay_2 correpond delay time before do anything else
 */
{

  // Clear and set cursor
  if (clear == 1)
  {
    lcd.clear();
  }

  // Get the message
  int  i = 0;
  char message[16];
  while (i < 16)
  {
    message[i] = *(msg + i);
    lcd.setCursor(i,cursor);
    lcd.print(message[i]);
    //Serial.print(message[i]);
    delay(delay_1);
    i += 1;
  }
  delay(delay_2);
}


void printCompiledMessage(int number){
  /*
  * On appelle cette fonction pour afficher des messages récurrents
  */
  
  switch(number){
    
    case 1:
        strncpy(msg,"Identification   ",sizeof(msg));
        printLCD(&msg[0] , 0 , 1 , 100, 0 );
        strncpy(msg,"requise.        ",sizeof(msg));
        printLCD(&msg[0], 1, 0, 100, 50);
        break;
  
    case 2:
        strncpy(msg,"Vous etes       ",sizeof(msg));
        printLCD(&msg[0] , 0 , 1 , 30, 0 );
        strncpy(msg,"connecte.       ",sizeof(msg));
        printLCD(&msg[0], 1, 0, 30, 0);
        break;
  }
}


//  ##################################
//  #         RFID Functions         #
//  ##################################

boolean readRFID()
/*
* Lit le rfid et retourne true si la puce envoies la même MASTERKEY que 
* celle enregistré
*/
{

  if (monModuleRFID.isCard())
  {
    // Get the id card
    if (monModuleRFID.readCardSerial())
    {
      for (int i = 0; i <= 4; i++)
      {
        UID[i] = monModuleRFID.serNum[i];
      }

      // Check if the identifier is authorized
      if (UID[0] == MASTERKEY[0] && UID[1] == MASTERKEY[1] && UID[2] == MASTERKEY[2] && UID[3] == MASTERKEY[3] && UID[4] == MASTERKEY[4])
      {

        return true;
      }
    }
  }
  return false;
}

int changeLockerState(int locker)
/*
* Change la position du locker
* Imprimante utilisable ou non 
*/
{
  if (locker == 1)
  {
    return 0;
  }
  else if (locker == 0)
  {
    return 1;
  }
}
