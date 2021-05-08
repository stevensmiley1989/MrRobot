#include <SPI.h>

#include <nRF24L01.h>
#include <RF24.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
RF24 radio(9, 10); // CE, CSN

const byte address[6] = "00001";
const byte slaveAddress[5] = {'R','x','A','A','A'};
unsigned long lastReceiveTime = 0;
unsigned long cTime = 0;
struct Data_Package {
  byte clamp_d;
  byte roll_d;
  byte pitch_d;
  byte yaw_d;
};
Data_Package data; //Create a variable with the above structure
int counter = 0;
int finger = 0; //finger thumb
int finger_Data = A0;
int finger_high = 100;
int finger_low = 0;
float finger_high_range = 0;
float finger_low_range = 0;
int finger_high_range_int= 0;
int finger_low_range_int=0;
float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float accAngleX, accAngleY, gyroAngleX, gyroAngleY, gyroAngleZ;
float roll, pitch, yaw;
float AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ;
float elapsedTime, currentTime, previousTime;
unsigned int adata = 0;
//How often to send values to the Robotic Arm
int response_time = 0.1;
int c = 0;



void setup() {
  //Serial.begin(9600);
  Serial.begin(115200);
  //Serial.begin(250000);
  radio.begin();
  
  radio.setAutoAck(false);
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.setRetries(15,15);//15,15
  radio.openWritingPipe(slaveAddress);
  //Note that one Arduino writes Sender.ino and the other writes Receiver.ino.
  //The identifier here is written to Sender.ino
  Serial.println("I'm Sender...");
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  calculate_finger_max();
}

void loop() {

  Serial.print("Sending packet: ");
  Serial.println(counter);
  finger = analogRead(finger_Data);
  Serial.println("Finger");
  Serial.println(finger);
  //send_data();
  finger=map(finger,finger_low_range_int,finger_high_range_int,0,100);//Map value 590-630,800-950 to 0-100
  if (finger >= finger_high) {
    Serial.println("unclamp");
    data.clamp_d=0;
  }

  if (finger <= finger_low) {
    Serial.println("clamp");
    data.clamp_d=255;
  }

  //}
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  AccErrorX = 0.0;
  AccErrorY = 0.0;
  AccX=a.acceleration.x;
  AccY=a.acceleration.y;
  AccZ=a.acceleration.z;
  
  accAngleX = (atan(AccY / sqrt(pow(AccX,2) + pow(AccZ, 2))) * 180 / PI) - AccErrorX;
  accAngleY = (atan(-1 * AccX / sqrt(pow(AccY, 2) + pow(AccZ, 2))) * 180 / PI) - AccErrorY;
  // === Read gyroscope data === //
  previousTime = currentTime;        // Previous time is stored before the actual time read
  currentTime = millis();            // Current time actual time read
  elapsedTime = (currentTime - previousTime) / 1000; // Divide
  //GyroX = GyroX + 1.86; // GyroErrorX ~(-1.86)
  GyroErrorX = 0.0;
  GyroErrorY = 0.0;
  GyroErrorZ = 0.0;
  GyroX = g.gyro.x;
  GyroY = g.gyro.y;
  GyroZ = g.gyro.z;
  GyroX = GyroX - GyroErrorX;
  //GyroY = GyroY - 2.47; // GyroErrorY ~(2.47)
  GyroY = GyroY - GyroErrorY;
  //GyroZ = GyroZ - 0.46; // GyroErrorZ ~ (0.46)
  GyroZ = GyroZ - GyroErrorZ;

  // Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
  gyroAngleX = gyroAngleX + GyroX * elapsedTime; // deg/s * s = deg
  gyroAngleY = gyroAngleY + GyroY * elapsedTime;
  yaw =  yaw + GyroZ * elapsedTime;

  // Complementary filter - combine acceleromter and gyro angle values
  gyroAngleX = 0.5 * gyroAngleX + 0.5 * accAngleX;
  gyroAngleY = 0.5 * gyroAngleY + 0.5 * accAngleY;

  roll=gyroAngleX;
  pitch=gyroAngleY;
  /* Print out the values */
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");
  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");
  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" degC");
  Serial.print(roll);
  Serial.print("/");
  Serial.print(pitch);
  Serial.print("/");
  Serial.println(yaw);
  Serial.println("");

  data.roll_d=map(roll,-90,+90,0,255);
  data.pitch_d=map(pitch,-90,+90,0,255);
  data.yaw_d=map(yaw,-90,+90,0,255);
  // Send the whole data from the structure to the receiver
  //Serial.println(String(data.roll_d));
  radio.write(&data, sizeof(Data_Package));
  //delay(1000);
}


void calculate_finger_max() {
  // We can call this funtion in the setup section so we can get our finger min and max values on the sensor.
  int numtimes = 200;
  while (c < numtimes) {
    finger = analogRead(finger_Data);
    finger_high_range+=finger;
    c++;}
  finger_high_range=finger_high_range/numtimes;
  finger_high_range_int=int(finger_high_range);
  finger_low_range=0.95*finger_high_range;
  finger_low_range_int=int(finger_low_range);
  Serial.print("finger_high_range: ");
  Serial.println(finger_high_range_int);
  Serial.print("finger_low_range: ");
  Serial.println(finger_low_range_int);
  }
