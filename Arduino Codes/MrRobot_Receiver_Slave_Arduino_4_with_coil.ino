#include <Wire.h>
#define SLAVE_ADDR 8


// Include the AccelStepper library:
#include <AccelStepper.h>
// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1
//int limit = 10; // ASSUME LIMIT-SWITCH IS PLACED AT RIGHT CORNER
int x=0;
int y=0;

boolean madestep;
boolean reversestep;
boolean charging;
boolean stepping;
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

// zoomkat 8-6-10 serial I/O string test
// type a string in serial monitor. then send or enter
// for IDE 0019 and later

//A very simple example of sending a string of characters
//from the serial monitor, capturing the individual
//characters into a String, then evaluating the contents
//of the String to possibly perform an action (on/off board LED).

int Relay1 = 4;
int Relay2 = 5;
int Relay3 = 7;
int Relay4 = 6;
int Relay5 = 11;
int Relay6  = 12;



float StartTime_Charge;
float StartTime_Trigger;
float StartTime_Hold;
float StartTime_spin;
float CurrentTime;
float ElapsedTime_Charge;
float ElapsedTime_Trigger;
float ElapsedTime_Hold;
float ElapsedTime_spin;

String readString;

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onReceive(get_relay_i2c);
  Serial.begin(9600);
  //pinMode(limit,INPUT);
  stepper.setMaxSpeed(1000);//
  stepper.setAcceleration(2000); //

  pinMode(Relay1, OUTPUT);
  pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT);
  pinMode(Relay4, OUTPUT);
  pinMode(Relay5, OUTPUT);
  pinMode(Relay6, OUTPUT);
  digitalWrite(Relay1,HIGH);
  digitalWrite(Relay2,HIGH);
  digitalWrite(Relay3,LOW);
  digitalWrite(Relay4,HIGH);
  digitalWrite(Relay5,HIGH);
  digitalWrite(Relay6,HIGH);
  madestep=false;
  stepping=false;
}





  
void step_to() {
  x=0;
  do{
    //check_time();
    x+=1;
    y=y+x;
    stepper.moveTo(y);
    //stepper.runToPosition();
    stepper.setSpeed(100);
    stepper.runSpeedToPosition();
    if(x>80){
      digitalWrite(Relay4, LOW);
      delay(1000);
      digitalWrite(Relay4, HIGH);
      digitalWrite(Relay3, LOW);
      digitalWrite(Relay1, HIGH);
      Serial.println("Relay1 OFF");
      delay(1000);
      digitalWrite(Relay6,LOW);
      stepping=false;
    break;}
    Serial.print('x');
    Serial.println(x);
    }while(stepping==true);}

void loop() {
  if(stepping==true){step_to();};
  ;}
  

void charge_func(){
      digitalWrite(Relay4, HIGH);
      digitalWrite(Relay3, LOW);
      digitalWrite(Relay1, HIGH);
      Serial.println("Relay1 OFF");
      digitalWrite(Relay2, LOW);
      Serial.println("Relay2 ON");
      StartTime_Charge = micros()/1000000.;
      charging=true;
}


void get_relay_i2c(){
  while (0 <Wire.available()) {
    delay(3); 
    char c = Wire.read();
    readString += c;
  }

//////////////////////
    if(readString.indexOf("10") >=0) //on1 = case 10
    {
      digitalWrite(Relay1, HIGH);
      Serial.println("Relay1 ON");
    }
    if(readString.indexOf("11") >=0) //off1 = case 11
    {
      digitalWrite(Relay1, LOW);
      Serial.println("Relay1 OFF");
    }
//////////////////////
    if(readString.indexOf("20") >=0) //on2 = case 20
    {
      digitalWrite(Relay2, HIGH);
      Serial.println("Relay2 ON");
    }

    if(readString.indexOf("21") >=0) //off2= case 21
    {
      digitalWrite(Relay2, LOW);
      Serial.println("Relay2 OFF");
    }
////////////////////////
    if(readString.indexOf("30") >=0) //on3 = case 30
    {
      digitalWrite(Relay3, HIGH);
      Serial.println("Relay3 ON");
    }

    if(readString.indexOf("31") >=0) //off3 = case 31
    {
      digitalWrite(Relay3, LOW);
      Serial.println("Relay3 OFF");
    }
////////////////////////
    if(readString.indexOf("40") >=0) //on4 = case 40
    {
      digitalWrite(Relay4, HIGH);
      Serial.println("Relay4 ON");
    }

    if(readString.indexOf("41") >=0) //off4 = case 41
    {
      digitalWrite(Relay4, LOW);
      Serial.println("Relay4 OFF");
    }

////////////////////////
    if(readString.indexOf("50") >=0) //on5 = case 50
    {
      digitalWrite(Relay5, HIGH);
      Serial.println("Relay5 ON");
    }

    if(readString.indexOf("51") >=0) //off5 = case 51
    {
      digitalWrite(Relay5, LOW);
      Serial.println("Relay5 OFF");
    }
///////////////
////////////////////////
    if(readString.indexOf("60") >=0) //on6 = case 60
    {
      digitalWrite(Relay6, HIGH);
      Serial.println("Relay6 ON");
    }

    if(readString.indexOf("61") >=0) //off6 = case 61
    {
      digitalWrite(Relay6, LOW);
      Serial.println("Relay6 OFF");
    }
///////////////
//////////////////
    if(readString.indexOf("71") >=0) //trigger = case 71
    {
      digitalWrite(Relay4, HIGH);
      digitalWrite(Relay6, HIGH);
      digitalWrite(Relay3, LOW);
      Serial.println("Relay3 ON");
      digitalWrite(Relay1, LOW);
      Serial.println("Relay1 ON");
      digitalWrite(Relay2, HIGH);
      Serial.println("Relay2 OFF");
     // madestep=false;
     // reversestep=false;
     // x=0;
      //StartTime_spin = micros()/1000000.;
     // CurrentTime = micros()/1000000.;
      //StartTime_Trigger = micros()/1000000.;
      //delay(1000);
      //charge_func();

    }
///////////////////////
    if(readString.indexOf("72") >=0) //charge = case 72
    {
      digitalWrite(Relay4, HIGH);
      digitalWrite(Relay3, LOW);
      digitalWrite(Relay1, HIGH);
      Serial.println("Relay1 OFF");
      digitalWrite(Relay2, LOW);
      Serial.println("Relay2 ON");
      StartTime_Charge = micros()/1000000.;
      charging=true;
    }
//////////////////////
    if(readString.indexOf("73") >=0) //reset = case 73
    {
      digitalWrite(Relay1, HIGH);
      Serial.println("Relay1 OFF");
      digitalWrite(Relay2, HIGH);
      Serial.println("Relay2 OFF");
    }
    if(readString.indexOf("74") >=0) //step_to = case 75
    {
      x=0;
      stepping=true;
      //step_to();

      
    }
    readString="";
  }
