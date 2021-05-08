// Include SPI library for nRF24L01
#include <SPI.h>
// Include nRF24L01 library for nRF24L01
#include <nRF24L01.h>
// Include RF24 library for nRF24L01
#include <RF24.h>
// Include Arduino Wire library for I2C
#include <Wire.h>
// Define Slave I2C Address
#define SLAVE_ADDR 9
// Define Slave I2C Address
#define SLAVE_ADDR2 8
RF24 radio(9, 10);   // nRF24L01 (CE, CSN)
const byte thisSlaveAddress[5] = {'R','x','A','A','A'};
unsigned long lastReceiveTime = 0;
unsigned long currentTime = 0;
float roll; //MPU6050 roll
float clamp_status; //gripper open/close status
float pitch; //MPU6050 pitch
float yaw; //MPU6050 yaw
struct Data_Package {   //Data array for storing MPU6050 received values of roll,pitch,yaw, and transmitted values for gripper
  byte clamp_d;
  byte roll_d;
  byte pitch_d;
  byte yaw_d;
};
Data_Package data; //Create a variable with the above structure

int angle = 180;// initial angle for Gripper

const byte numChars = 32; //character limit
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;
int relay_flashlight = 8; // pin for flashlight relay
int relay_laser=6; // pin for laser relay
boolean relayState_flashlight = false;//initially off
boolean relayState_laser =false; //initially off
String coilstring; //string for sending case_i value
String case_i; //coil gun case
// Define counter to count bytes in response
int bcount;
 
// Define array for return data
byte distance[5];
 
void setup()
{
  Wire.begin();
  pinMode(relay_flashlight,OUTPUT);
  digitalWrite(relay_flashlight,HIGH);
  pinMode(relay_laser,OUTPUT);
  digitalWrite(relay_laser,HIGH);
  Serial.begin(115200); //baudrate should match Raspberry Pi code
  coilstring="";
  case_i="";
//Note that one Arduino writes Sender.ino and the other writes Receiver.ino.
//To identify the program written in Receiver.ino.
Serial.println("I'm Receiver...");
  radio.begin();
  radio.openReadingPipe(0, thisSlaveAddress);
  radio.setAutoAck(false);
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening(); //  Set the module as receiver
  radio.setRetries(15,15);
}

void recvWithEndMarker() {
 static byte ndx = 0;
 char endMarker = '\n';
 char rc;
 
 // if (Serial.available() > 0) {
           while (Serial.available() > 0 && newData == false) {
 rc = Serial.read();

 if (rc != endMarker) {
 receivedChars[ndx] = rc;
 ndx++;
 if (ndx >= numChars) {
 ndx = numChars - 1;
 }
 }
 else {
 receivedChars[ndx] = '\0'; // terminate the string
 ndx = 0;
 newData = true;
 }
 }
}

void showNewData() {
 if (newData == true) {
 Serial.print("This just in ... ");
 Serial.println(receivedChars);
case_i=String(receivedChars);
//////////////////////
    if(case_i.indexOf("on1") >=0) //on1 = case 10
    {
     coilstring="10";
     Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
     Wire.write(coilstring.c_str());  /* sends hello string */
     Wire.endTransmission(); 
     Serial.println("Relay1 ON");
    }
    if(case_i.indexOf("off1") >=0) //off1 = case 11
    {
     coilstring="11";
     Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
     Wire.write(coilstring.c_str());  /* sends hello string */
     Wire.endTransmission(); 
     Serial.println("Relay1 OFF");
    }
//////////////////////
    if(case_i.indexOf("on2") >=0) //on2 = case 20
    {
      coilstring="20";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay2 ON");
    }

    if(case_i.indexOf("off2") >=0) //off2= case 21
    {
      coilstring="21";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay2 OFF");
    }
////////////////////////
    if(case_i.indexOf("on3") >=0) //on3 = case 30
    {
      coilstring="30";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay3 ON");
    }

    if(case_i.indexOf("off3") >=0) //off3 = case 31
    {
      coilstring="31";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay3 OFF");
    }
////////////////////////
    if(case_i.indexOf("on4") >=0) //on4 = case 40
    {
      coilstring="40";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission();       
      Serial.println("Relay4 ON");
    }

    if(case_i.indexOf("off4") >=0) //off4 = case 41
    {
      coilstring="41";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay4 OFF");
    }

////////////////////////
    if(case_i.indexOf("on5") >=0) //on5 = case 50
    {
      coilstring="50";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay5 ON");
    }

    if(case_i.indexOf("off5") >=0) //off5 = case 51
    {
      coilstring="51";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay5 OFF");
    }
///////////////
////////////////////////
    if(case_i.indexOf("on6") >=0) //on6 = case 60
    {
      coilstring="60";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay6 ON");
    }

    if(case_i.indexOf("off6") >=0) //off6 = case 61
    {
      coilstring="61";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay6 OFF");
    }
///////////////
//////////////////
    if(case_i.indexOf("trigger") >=0) //trigger = case 71
    {
      coilstring="71";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 

      Serial.println("Relay3 ON");

      Serial.println("Relay1 ON");

      Serial.println("Relay2 OFF");


    }
///////////////////////
    if(case_i.indexOf("charge") >=0) //charge = case 72
    {
      coilstring="72";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay1 OFF");
      Serial.println("Relay2 ON");
    }
//////////////////////
    if(case_i.indexOf("reset") >=0) //reset = case 73
    {
      coilstring="73";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("Relay1 OFF");
      Serial.println("Relay2 OFF");
    }
    if(case_i.indexOf("step_to") >=0) //step_to = case 74
    {
      coilstring="74";
      Wire.beginTransmission(SLAVE_ADDR2); /* begin with device address 8 */
      Wire.write(coilstring.c_str());  /* sends hello string */
      Wire.endTransmission(); 
      Serial.println("stepping");
    }

    case_i="";
  
 
 char *step_az=strstr(receivedChars,"servo");
 step_az+=strlen("servo");
 char *step_azval=strtok(step_az,";");
 int step_valAZ = atoi(step_azval);
 //Serial.println(valAZ);
 if (step_valAZ!=29939){
  angle=180-step_valAZ;
  //Serial.println(angle);
  String thisString  = String(angle);
  Wire.beginTransmission(SLAVE_ADDR); /* begin with device address 8 */
  Wire.write(thisString.c_str());  /* sends hello string */
  Wire.endTransmission();    /* stop transmitting */}

 char *flash_az=strstr(receivedChars,"flashlight");
 flash_az+=strlen("flashlight");
 char *flash_azval=strtok(flash_az,";");
 int flash_valAZ = atoi(flash_azval); //'0' is off, '1' is on
 //Serial.println(valAZ);
 char *laser_az=strstr(receivedChars,"laser");
 laser_az+=strlen("laser");
 char *laser_azval=strtok(laser_az,";");
 int laser_valAZ = atoi(laser_azval); //'0' is off, '1' is on
 
 if (flash_valAZ==1){
  relayState_flashlight=true;
  if (relayState_laser==false){
    digitalWrite(relay_flashlight,LOW);
    digitalWrite(relay_laser,HIGH);}
  else if(relayState_laser==true){
    digitalWrite(relay_flashlight,LOW);
    digitalWrite(relay_laser,LOW);}
  relayState_flashlight=true;
  }
 else if(flash_valAZ==0){
  relayState_flashlight=false;
  if(relayState_laser==false){
    digitalWrite(relay_flashlight,HIGH);
    digitalWrite(relay_laser,HIGH);}
  else if(relayState_laser==true){
    digitalWrite(relay_flashlight,HIGH);
    digitalWrite(relay_laser,LOW);}
   relayState_flashlight=false;
  }

 //Serial.println(valAZ);
 if (laser_valAZ==1){
  relayState_laser=true;
  if(relayState_flashlight==false){
    digitalWrite(relay_laser,LOW);
    digitalWrite(relay_flashlight,HIGH);}
  else if(relayState_flashlight==true){
    digitalWrite(relay_laser,LOW);
    digitalWrite(relay_flashlight,LOW);}
  relayState_laser=true;
  }
 else if(laser_valAZ==0){
  relayState_laser=false;
  if(relayState_flashlight==false){
    digitalWrite(relay_laser,HIGH);
    digitalWrite(relay_flashlight,HIGH);}
  else if(relayState_flashlight==true){
    digitalWrite(relay_laser,HIGH);
    digitalWrite(relay_flashlight,LOW);}
  relayState_laser=false;
  } 
 newData = false;
 }
}
byte readI2C(int address) {
  // Define a variable to hold byte of data
  byte bval ;
  long entry = millis();
  // Read one byte at a time
  Wire.requestFrom(address, 1); 
  // Wait 100 ms for data to stabilize
  while (Wire.available() == 0 && (millis() - entry) < 100)  ;//Serial.print("Waiting");
  recvWithEndMarker();
  showNewData();
  //servo_test.write(angle);              //command to rotate the servo to the specified angle
  // Place data into byte
  if  (millis() - entry < 100) bval = Wire.read();
  return bval;
}
 
void loop()
{
  recvWithEndMarker();
  showNewData();
// Check whether there is data to be received
    if (radio.available()) {
      radio.read(&data, sizeof(Data_Package)); // Read the whole data and store it into the 'data' structure
      //lastReceiveTime = millis(); // At this moment we have received the data
      roll=map(data.roll_d,0,255,-90,90);
      pitch=map(data.pitch_d,0,255,-90,90);
      yaw=map(data.yaw_d,0,255,-90,90);
      clamp_status=map(data.clamp_d,0,255,0,1);
  }
  Serial.println();
  Serial.print("\t Roll: ");
  Serial.print(roll);
  Serial.print(";  Pitch: ");
  Serial.print(pitch);
  Serial.print(";  clamp_status: ");
  Serial.print(clamp_status);
  Serial.println(";");
  while (readI2C(SLAVE_ADDR) < 255) {
  // Until first byte has been received sits in this loop

  }
  for (bcount = 0; bcount < 5; bcount++) {
    distance[bcount] = readI2C(SLAVE_ADDR);
  }
  for (int i = 0; i < 5; i++) {
    Serial.print(distance[i]);
    Serial.print("\t");
    Serial.print(";");
  }
  Serial.println();
}
