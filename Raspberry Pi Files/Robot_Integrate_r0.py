#Import Libraries
import signal
import warnings
warnings.filterwarnings('ignore')
import sys
import RPi.GPIO as GPIO
import time
import datetime
import os
import random
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
from gtts import gTTS
import os

#Definition of  motor pins on respective L298N
#L298N for Front two wheel's DC motors
IN1 = 16 #Front Left Forward
IN2 = 18 #Front Left Backward
IN3 = 26 #Front Right Forward #On L298N, IN3 and IN4 are swapped because of how Positive and Negative are connected to DC Motor
IN4 = 24 #Front Right Backward #On L298N, IN3 and IN4 are swapped because of how Positive and Negative are connected to DC Motor
ENA = 32 #Front Left Power
ENB = 19 #Front Right Power
IN5 = 23 #Back Left Forward
IN6 = 21 #Back Left Backward
IN7 = 29 #Back Right Forward #On L298N, IN7 and IN8 are swapped because of how Positive and Negative are connected to DC Motor
IN8 = 31 #Back Right Backward #On L298N, IN7 and IN8 are swapped because of how Positive and Negative are connected to DC Motor
ENC = 11 #Back Left Power
END = 15 #Back Right Power

#Definition of servo pins
# Servos 1 & 3
# Coil gun arm has two servos connected together to move the coil gun up and down
Servo1 = 36
Servo3 = 38
# Servos 6 & 7 
# Gripper has two servos connected together to move the bottom gripper up and down 
Servo6 = 12
Servo7 = 33
# Servos 2,4 & 5 are not used
#Servo2 = 38 
#Servo4 = 37 
#Servo5 = 35


#Set the GPIO port to BOARD encoding mode
GPIO.setmode(GPIO.BOARD)                       #Set GPIO pin numbering

#Ignore warning information
GPIO.setwarnings(False)

def reset():
    #Resets all of the gpio pin
    os.system('sudo chmod 777 initpin.sh')
    os.system('./initpin.sh')
reset()


def folder_path(path):
    # This function takes a desired filepath, path, and tries to make a directory for it
    # path: dtype = string
    try:
        os.mkdir(path)
    except OSError:
        return(path)
    else:
        return(path)
    return(path)
    

def init():
    #Motor pins are initialized into output mode
    #Key pin is initialized into input mode
    #Ultrasonic pin,RGB pin,servo pin initialization
    global pwm_ENA
    global pwm_ENB
    global pwm_ENC
    global pwm_END
    global pwm_servo_1
    #global pwm_servo_2
    global pwm_servo_3
    global pwm_servo_4
    #global pwm_servo_5
    global pwm_servo_6
    global pwm_servo_7
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENC,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN5,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN6,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(END,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN7,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN8,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(Servo1, GPIO.OUT)
    #GPIO.setup(Servo2, GPIO.OUT)
    GPIO.setup(Servo3, GPIO.OUT)
    #GPIO.setup(Servo4, GPIO.OUT)
    #GPIO.setup(Servo5, GPIO.OUT)
    GPIO.setup(Servo6, GPIO.OUT)
    GPIO.setup(Servo7, GPIO.OUT)
    #Set the PWM pin and frequency is 10000hz
    pwm_ENA = GPIO.PWM(ENA, 10000)
    pwm_ENB = GPIO.PWM(ENB, 10000)
    pwm_ENC = GPIO.PWM(ENC, 10000)
    pwm_END = GPIO.PWM(END, 10000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    pwm_ENC.start(0)
    pwm_END.start(0)

    pwm_servo_1 = GPIO.PWM(Servo1, 50)
    pwm_servo_1.start(0)
    #pwm_servo_2 = GPIO.PWM(Servo2, 50)
    #pwm_servo_2.start(0)
    pwm_servo_3=GPIO.PWM(Servo3,50)
    pwm_servo_3.start(0)
    #pwm_servo_4=GPIO.PWM(Servo4,50)
    #pwm_servo_4.start(0)
    #pwm_servo_5=GPIO.PWM(Servo5,50)
    #pwm_servo_5.start(0)
    pwm_servo_6=GPIO.PWM(Servo6,50)
    pwm_servo_6.start(0)
    pwm_servo_7=GPIO.PWM(Servo7,50)
    pwm_servo_7.start(0)
    
currentDirectory=os.getcwd()
print(currentDirectory)

def run(leftspeed, rightspeed):
    #go forward
    #leftspeed: dtype=int,desc=ranges 0 to 100
    #rightspeed: dtype=int, desc=ranges 0 to 100
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)    
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)


def back(leftspeed, rightspeed):
    #back
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.HIGH)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)
    

def left(leftspeed, rightspeed):
    #turn left
    #leftspeed: dtype=int,desc=ranges 0 to 100
    #rightspeed: dtype=int, desc=ranges 0 to 100
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)

 
def right(leftspeed, rightspeed):
    #turn right
    #leftspeed: dtype=int,desc=ranges 0 to 100
    #rightspeed: dtype=int, desc=ranges 0 to 100
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)
    

def spin_left(leftspeed, rightspeed):
    #turn left in place
    #leftspeed: dtype=int,desc=ranges 0 to 100
    #rightspeed: dtype=int, desc=ranges 0 to 100
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.HIGH)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)


def spin_right(leftspeed, rightspeed):
    #turn right in place
    #leftspeed: dtype=int,desc=ranges 0 to 100
    #rightspeed: dtype=int, desc=ranges 0 to 100
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    pwm_ENC.ChangeDutyCycle(leftspeed)
    pwm_END.ChangeDutyCycle(rightspeed)


def brake():
   #brake
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)
   GPIO.output(IN5, GPIO.LOW)
   GPIO.output(IN6, GPIO.LOW)
   GPIO.output(IN7, GPIO.LOW)
   GPIO.output(IN8, GPIO.LOW)

#The servo rotates to the specified angle
#def servo_1(pos,hold=False):
#    for i in range(18):
#        pwm_servo_1.ChangeDutyCycle(2 + 10 * pos/180)
#    time.sleep(1) #0.7
#    if hold==False:
#        pwm_servo_1.start(0)
        
#The servo rotates to the specified angle
#def servo_2(pos,hold=False):
#    for i in range(18):
#        pwm_servo_2.ChangeDutyCycle(2 + 10 * pos/180)
#    time.sleep(1)
#    if hold==False:
#        pwm_servo_2.start(0)

#def servo_3(pos,hold=False):
#    for i in range(18):
#        pwm_servo_3.ChangeDutyCycle(2 + 10 * pos/180)
#    time.sleep(1)
#    if hold==False:
#        pwm_servo_3.start(0)
#def servo_4(pos,hold=False):
#    for i in range(18):
#        pwm_servo_4.ChangeDutyCycle(2 + 10 * pos/180)
#    time.sleep(1)
#    if hold==False:
#        pwm_servo_4.start(0)

def servo_1_3(pos,hold=False):
    # Servos 1 & 3
    # Coil gun arm has two servos connected together to move the coil gun up and down
    # This function takes the desired position (pos)in degrees and
    # moves both Servo motors 1 & 3 together by that amount
    # pos: dtype=int,desc= degrees
    # hold: dtype=boolean, desc= True/False ; If True, then holds the servos in position, which could cause jitter, but keeps position.
    #                          ; If False, then the servos could drift depending on the load, but is more stable.
    if pos<90:
        pos=90
    if pos>160:
        pos=160
    pos3=pos
    pos=180-pos
    pwm_servo_1.ChangeDutyCycle(2+10*pos/180)
    pwm_servo_3.ChangeDutyCycle(2+10*pos3/180)
    time.sleep(1)
    if hold==False:
        pwm_servo_1.start(0)
        pwm_servo_3.start(0)
        
#def servo_4_5(pos,hold=False):        
#    pos5=pos
#    pos=180-pos
#    for i in range(18):
#        pwm_servo_4.ChangeDutyCycle(2+10*pos/180)
#        pwm_servo_5.ChangeDutyCycle(2+10*pos5/180)
#    time.sleep(1)
#    if hold==False:
#        pwm_servo_4.start(0)
#        pwm_servo_5.start(0)

def servo_6_7(pos,hold=False):
    # Servos 6 & 7 
    # Gripper has two servos connected together to move the bottom gripper up and down 
    # This function takes the desired position (pos)in degrees and
    # moves both Servo motors 6 & 7 together by that amount
    # pos = degrees
    # hold = True/False ; If True, then holds the servos in position, which could cause jitter, but keeps position.
    #                   ; If False, then the servos could drift depending on the load, but is more stable.
    if pos>90:
        pos=90
    elif pos<0:
        pos=0
    #pos3=180-pos
    pos6=pos
    pos=180-pos
    #print('angle is {}'.format(angle13))
    for i in range(18):
        pwm_servo_6.ChangeDutyCycle(2+10*pos/180)
        pwm_servo_7.ChangeDutyCycle(2+10*pos6/180)
    time.sleep(1)
    if hold==False:
        pwm_servo_6.start(0)
        pwm_servo_7.start(0)
      
  

  


