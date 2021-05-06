
#include <Servo.h>             //Servo library 
Servo servo_test;        //initialize a servo object for the connected servo  
             
// Include NewPing Library for HC-SR04 sensor
#include <NewPing.h>
 
// Include Arduino Wire library for I2C
#include <Wire.h>
 
// Define Slave I2C Address
#define SLAVE_ADDR 9
 
// Hook up 4 HC-SR04 sensors in 1-pin mode
// Sensor 0
#define TRIGGER_PIN_0  8
#define ECHO_PIN_0     8
 
// Sensor 1
#define TRIGGER_PIN_1  9
#define ECHO_PIN_1     9
 
// Sensor 2
#define TRIGGER_PIN_2  10
#define ECHO_PIN_2     10
 
// Sensor 3
#define TRIGGER_PIN_3  11
#define ECHO_PIN_3     11

// Sensor 4
#define TRIGGER_PIN_4  7
#define ECHO_PIN_4     7
 
// Maximum Distance is 260 cm
#define MAX_DISTANCE 260
 
// Create objects for ultrasonic sensors
NewPing sensor0(TRIGGER_PIN_0, ECHO_PIN_0, MAX_DISTANCE);
NewPing sensor1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sensor2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE);
NewPing sensor3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE);
NewPing sensor4(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE);
int angle = 180;    
const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;
// Define return data array, one element per sensor
int distance[5];
 
// Define counter to count bytes in response
int bcount = 0;
 
void setup() {
 
  // Initialize I2C communications as Slave
  Wire.begin(SLAVE_ADDR);
 
   // Function to run when data requested from master
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent); /* register receive event */ 
  servo_test.attach(12);      // attach the signal pin of servo to 
  
}
// function that executes whenever data is received from master
String inString = ""; //string to hold input
void receiveEvent(int howMany) {
 while (0 <Wire.available()) {
    char c = Wire.read();      /* receive byte as a character */
    inString+=c;
  }
 angle=inString.toInt();
 inString="";
} 
void requestEvent() {
 
  // Define a byte to hold data
  byte bval;
  
  // Cycle through data
  // First response is always 255 to mark beginning
  switch (bcount) {
    case 0:
      bval = 255;
      break;
    case 1:
      bval = distance[0];
      break;
    case 2:
      bval = distance[1];
      break;
    case 3:
      bval = distance[2];
      break;
    case 4:
      bval = distance[3];
      break;
    case 5:
      bval = distance[4];
      break;
  }
  
  // Send response back to Master
  Wire.write(bval);
  
  // Increment byte counter
  bcount = bcount + 1;
  if (bcount > 5) bcount = 0;
 
}
 
void readDistance()
{
  distance[0] = sensor0.ping_cm();
  if (distance[0] > 254 ) {
    distance[0] = 254;
  }
  delay(20);
  
  distance[1] = sensor1.ping_cm();
  if (distance[1] > 254 ) {
    distance[1] = 254;
  }
  delay(20);
  
  distance[2] = sensor2.ping_cm();
  if (distance[2] > 254 ) {
    distance[2] = 254;
  }
  delay(20);
  
  distance[3] = sensor3.ping_cm();
  if (distance[3] > 254 ) {
    distance[3] = 254;
  }
  delay(20);
  
  distance[4] = sensor4.ping_cm();
  if (distance[4] > 254 ) {
    distance[4] = 254;
  }
  delay(20);  
  
}

 
void loop()
{
  servo_test.write(angle); 
  //Serial.print(angle);
  //Serial.println();
  // Refresh readings every half second
  readDistance();
  delay(50);
}
