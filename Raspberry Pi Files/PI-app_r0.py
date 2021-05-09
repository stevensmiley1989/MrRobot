##Initialize Variables and Import Libraries
# Debugging Logic
print_servo=False
print_ultrasonic=False
aim=False
grab=False

# MQTT Mosquitto Server/Client
clientName = "RPI4"
serverAddress = '192.168.1.30'

# Limit Switch GPIO Pin
limit_switch=22

# IR Sensor GPIO Pin
IR_sensor=37

# Servo Motors Global Variables
global servo_1_3 # Coil Gun Arm Servos
global servo_1_3_min, servo_1_3_max #min and max values
global servo_1_3_old #holds previous value
global servo_1_3_load_position #holds caliberated value for loading the coil gun
servo_1_3=180 # initially all the way up with value of 180
servo_1_3_min=90 # lower bound per calibration
servo_1_3_max=160 # upper bound per calibration
servo_1_3_old=0 # initially set to 0
servo_1_3_load_position=138 #calibrated value for loading coil gun

global servo_6_7 # Gripper Arm Servos
global servo_6_7_min, servo_6_7_max #min and max values
servo_6_7=90 # initially all the way down with value of 180
servo_6_7_min=0 # lower bound per calibration
servo_6_7_max=90 # upper bound per calibration

global servo_2 # Gripper
servo_2=0 # initially open a full 180 degrees by setting to 0

import numpy as np
def clip(theta,min_theta=0,max_theta=180):
    theta=int(np.clip(theta,min_theta,max_theta))
    return theta

# y_steps
global y_steps #used to move Servo_1_3 for Coil Gun arm in y direction
y_steps=0; #initial value for moving in the y direction of Servo_1_3 with exception

# Serial logic for Relays to Flashlight and Laser
flashlight=0# initially off=0; 
laser=0# initially off=0;

# Logic for Robot to use AI tracking to move
follow=0# initially do not follow=0;
follow_previous=follow #variable for previous position;

# Logic for Glove controlled through Serial with Arduino and NRF24L01
glove=0 # initially not controlled by glove=0;
glove_previous=glove #variable for previous value;

# Logic for Robot to use AI to fetch
fetch=0# initially not fetching=0;
fetch_previous=fetch#variable for previous value;

import time,math
import RPi.GPIO as GPIO
#Set GPIO pin numbering
#Ignore warning information
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 
GPIO.setup([IR_sensor,limit_switch],GPIO.IN)
import play_sound_r0
import paho.mqtt.client as mqtt
import Serial_Connect_Stepper_r0 as SS

import Robot_Integrate_r0 as RI
RI.init()
RI.servo_1_3(servo_1_3)

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/gpio")
left_ultrasonic=80
front_top_ultrasonic=80
front_bottom_ultrasonic=80
right_ultrasonic=80
back_ultrasonic=80
roll=0
pitch=0
clamp_status=0
t_obj=1.
t_person=1.
currTime=time.time()
prevTime=currTime
ci=0
ci_y=0
just_here=False
#import RPi.GPIO as gpio
global moving
moving_f=False
moving_b=False
moving_l=False
moving_r=False
from multiprocessing import Process, Queue, Pipe
import TF_object_detection_r0 as TF
pi=Queue()
rq=Queue()
cam=Queue()
object_to_detect=Queue()
pic=Queue()
TF_p=Process(target=TF.init,args=((pi),(rq),(cam),(object_to_detect),(pic),))
TF_p.start()
make_voice=Queue()
play_sound_Process=Process(target=play_sound_r0.play_sound, args=(make_voice,))
play_sound_Process.start()
global distance
distance=10
import time
case=2 #initial case to run
def case_run(case):
    global fetch_type,option_status
    if case==1:   
        fetch_type="orange_ball"
        option_status="orange_ball"
    if case==2:
        fetch_type='reindeer'
        option_status='reindeer'
    if case==3:
        fetch_type='person'
        option_status='person'
    try:
        object_to_detect.put(option_status)
    except:
        print('could not put')
case_run(case)
SS.servo_flashlight_laser(servo_2,flashlight,laser)
pic_status="Picture_Off"
T_saw=time.time()
def messageDecoder(client, userdata, msg):
    global moving_f, moving_b
    global distance
    global servo_1_3_old
    global servo_1_3,servo_2,servo_6_7
    global flashlight,laser,follow,glove,follow_previous,glove_previous,fetch,fetch_previous
    global pic_status
    global aim,grab
    message = msg.payload.decode(encoding='UTF-8')
    print(message)
    #distance=RI.Distance_test()
    #RI.Distance_test()
    if message == 'case1':
        case=1
        case_run(case)
        print('Case 1 was just selected')
    if message == 'case2':
        case=2
        case_run(case)
        print('Case 2 was just selected')
    if message == 'case3':
        case=3
        case_run(case)
        print('Case 3 was  just selected')
    if message == "aim_on":
        aim=True
    if message == "aim_off":
        aim=False   
    if message == "grab":
        grab=True
    if message == "charge":
        SS.charge()
    if message == "step_to":
        SS.step_to()
    if message == "trigger":
        SS.trigger()
    if message == "reset":
        SS.reset()
        SS.on6()
    if message == "p_twentyfive":
        servo_6_7=servo_6_7+25
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "p_ten":
        servo_6_7=servo_6_7+10
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "p_five":
        servo_6_7=servo_6_7+5
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "p_one":
        servo_6_7=servo_6_7+1
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "m_twentyfive":
        servo_6_7=servo_6_7-25
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "m_ten":
        servo_6_7=servo_6_7-10
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "m_five":
        servo_6_7=servo_6_7-5
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "m_one":
        servo_6_7=servo_6_7-1
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    if message == "plus_twentyfive":
        servo_1_3=clip(servo_1_3+25,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "plus_ten":
        servo_1_3=clip(servo_1_3+10,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "plus_five":
        servo_1_3=clip(servo_1_3+5,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "plus_one":
        servo_1_3=clip(servo_1_3+1,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "minus_twentyfive":
        servo_1_3=clip(servo_1_3-25,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "minus_ten":
        servo_1_3=clip(servo_1_3-10,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "minus_five":
        servo_1_3=clip(servo_1_3-5,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "minus_one":
        servo_1_3=servo_1_3-1
        servo_1_3=clip(servo_1_3-1,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "Fetch_On":
        fetch=1 #sjs 4/10
        follow=1
        if option_status=='reindeer':
            servo_1_3=140
        elif option_status=='person':
            servo_1_3=150
        else:
            servo_1_3=150
        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    if message == "Picture_1":
        pic_status="Picture_1"
        pic.put(pic_status)
    if message == "Picture_On":
        pic_status="Picture_On"
        pic.put(pic_status)
    if message == "Picture_Off":
        pic_status="Picture_Off"
        pic.put(pic_status)
        
    if message == "Fetch_Off" or message == "Follow_on":
        fetch=0
        #follow=0
        if option_status=='reindeer':
            servo_1_3=120
        elif option_status=='person':
            servo_1_3=150
        else:
            servo_1_3=150
        RI.servo_1_3(servo_1_3)
    if message == "glove_on":
        glove=1
    if message == "glove_off":
        glove=0
    if message == "Follow_on":
        follow=1
        fetch_type='person'
    if message == "Follow_off":
        follow=0
    if message == "flashlight_on":
        flashlight=1
        laser=laser
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if message == "flashlight_off":
        flashlight=0
        laser=laser
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if message == "laser_on":
        flashlight=flashlight
        laser=1
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if message == "laser_off":
        flashlight=flashlight
        laser=0
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if message == "both_on":
        flashlight=1
        laser=1
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if message == "both_off":
        flashlight=0
        laser=0
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if moving_f==True and distance<2:
        RI.brake()
        moving=False
        print("Distance is {} and stopping".format(distance))
    if message == "run":
        print("running!")
        RI.run(100,100);
        moving_f=True
    elif message=="vert_180":
        servo_1_3=180
        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    elif message=="vert_90":
        servo_1_3=90
        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max);
        RI.servo_1_3(servo_1_3);
    elif message=="vert_0":
        servo_1_3=0
        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
        RI.servo_1_3(servo_1_3)
    elif message=="horiz_180":
        servo_6_7=180
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    elif message=="horiz_90":
        servo_6_7=90
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(90);
    elif message=="horiz_0":
        servo_6_7=0
        servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
        RI.servo_6_7(servo_6_7)
    elif message=="run_0.1":
        print("running 0.1 sec")
        RI.run(100,100);time.sleep(0.1);RI.brake()
    elif message=="back_0.1":
        print("backing up 0.1 sec")
        RI.back(100,100);time.sleep(0.1);RI.brake()
    elif message=="run_0.3":
        print("running 0.3 sec")
        RI.run(100,100);time.sleep(0.3);RI.brake()
    elif message=="back_0.3":
        print("backing up 0.3 sec")
        RI.back(100,100);time.sleep(0.3);RI.brake()
    elif message == "stop":
        print("stopping!")
        if moving_f==True:
            RI.run(20,20);time.sleep(0.3);RI.brake()
        if moving_b==True:
            RI.back(20,20);time.sleep(0.3);RI.brake()
        RI.brake();
        moving_f=False
        moving_b=False
    elif message=="SL_0.1":
        print("spinning left 0.1 sec")
        RI.spin_left(100,100);time.sleep(0.1);RI.brake()
    elif message=="SR_0.1":
        print("spinning right 0.1 sec")
        RI.spin_right(100,100);time.sleep(0.1);RI.brake()
    elif message == "back":
        print("backing up!")
        RI.back(100,100);
        moving_b=True
    elif message == "spinright":
        print("spinningright")
        RI.spin_right(100,100);
    elif message == "spinleft":
        print("spinningleft")
        RI.spin_left(100,100);
    elif message == "clamp":
        print("clamping")
        servo_2=180
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    elif message == "unclamp":
        print("unclamping")
        servo_2=0
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    elif message=="ser_Relax":
        try:
            RI.servo_1_3(servo_1_3)   
        except:
            servo_1_3=150
            servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
            RI.servo_1_3(servo_1_3)
        print("servo is relaxing")
    elif message=="grip_Relax":
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
        print("gripper is rlaxing")
    else:
        print(message)
    follow_previous=follow
 
mqttClient = mqtt.Client(clientName)
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder		
mqttClient.connect(serverAddress)
def deg_to_rad(angle):
    return angle*math.pi/180.0

def move_robot(x_AI,y_AI,x_AI_old,y_AI_old):
    global servo_1_3, fetch, option_status,fetch_type,servo_6_7,servo_1_3_load_position
    global t_obj,t_person, currTime, prevTime,ci,aim,ci_y,just_here
    global centered_on_obj,centered_on_human,just_saw,T_saw,y_steps
    currTime=time.time()
    if (currTime-prevTime)<5:
        deltaTime=currTime-prevTime
    else:
        deltaTime=0
    delta_error=abs(x_AI)-abs(x_AI_old)
    delta_error_y=abs(y_AI)-abs(y_AI_old)
    cp=abs(x_AI)
    cp_y=abs(y_AI)
    
    ci+=abs(x_AI)*deltaTime
    ci_y+=abs(y_AI)*deltaTime
    ki=0.0
    ki_y=0.0
    if deltaTime>0:
        cd=(delta_error/deltaTime)
        cd_y=(delta_error_y/deltaTime)
    else:
        cd=0
        cd_y=0
    kd=0.0
    kd_y=0.0
    prevTime=currTime
    
    if option_status==fetch_type and option_status!='person':
        kp=0.5
        t_obj=kp*cp+ki*ci+kd*cd
        print('t_obj',t_obj)
        if aim==True:
            if x_AI<-0.035:
                RI.spin_left(100,100);time.sleep(t_obj);RI.brake();
            elif x_AI>0.035:
                RI.spin_right(100,100);time.sleep(t_obj);RI.brake();
            else:
                t_obj=t_obj
        else:
            if x_AI<-0.035:
                RI.spin_left(100,100);time.sleep(t_obj);RI.brake();
            elif x_AI>0.035:
                RI.spin_right(100,100);time.sleep(t_obj);RI.brake();
            else:
                t_obj=t_obj
        if aim==True or fetch==1:
            kp_y=5 #5
            y_steps=kp_y*cp_y+ki_y*ci+kd_y*cd_y
            if y_AI==y_AI_old:
                pass
            elif y_AI<-0.075:
                servo_1_3-=y_steps;
                servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                #RI.servo_1_3(servo_1_3,True);
                just_here=False
                centered_on_object=False
            elif y_AI>0.075:
                servo_1_3+=y_steps;
                servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                #RI.servo_1_3(servo_1_3);
                just_here=False
                centered_on_object=False
            else:
                if just_here==False and aim==True:
                    RI.servo_1_3(servo_1_3_load_position);
                    SS.charge();
                    time.sleep(7);
                    SS.step_to();
                    time.sleep(4);
                    RI.servo_1_3(servo_1_3);
                    time.sleep(2);
                    SS.trigger();
                    RI.servo_1_3(servo_1_3);
                    just_here=True
                    centered_on_obj=True
                    pass
                elif just_here==False and aim==False:
                    if y_AI<0:
                        servo_1_3-=y_steps;
                        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                    elif y_AI>0:
                        servo_1_3+=y_steps;
                        servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                    centered_on_obj=True
                    just_here=True
                    T_saw=time.time()
                    pass
            
    if option_status=='person':
        kp=0.3
        t_person=kp*cp+ki*ci+kd*cd
        print('t_person',t_person)
        #t_person=t_person*abs(x_AI)
        if x_AI<-0.035:
            RI.spin_left(100,100);time.sleep(t_person);RI.brake();
        elif x_AI>0.035:
            RI.spin_right(100,100);time.sleep(t_person);RI.brake();
        else:
            t_person=t_person
            centered_on_human=True
            just_saw=True
        T_saw=time.time()
ready_status=True



import time
#time.sleep(3)
TI=time.time()
TI_old=TI
x_AI=0
x_AI_old=x_AI
y_AI=0
y_AI_old=y_AI
count_term=0
count_star=0
obj_count=0 #used to keep track of when AI switches from person to ball.
person_count=0 #used to keep track of when AI switches from ball to person.
limit_distance=120
just_saw=False #used to see if we saw the ball or not
obj_found=time.time()
T_back=time.time()
object_status='moving'
global count_put
count_put=0
count=0
count_person=0
cum_error_x=0
centered_on_human=False
centered_on_obj=False
avg_error_x=0
time_grabbed=time.time()
t_reset_servos=time.time()

while True:
    time_i=time.time()
    try:
        if GPIO.input(IR_sensor)==0:
            print('time to grab')
            servo_2=180
            SS.servo_flashlight_laser(servo_2,flashlight,laser)
    except:
        pass
    if GPIO.input(limit_switch)==0:
        print('hit the limit')
        servo_2=0
        SS.servo_flashlight_laser(servo_2,flashlight,laser)
    if servo_6_7!=45 and option_status=='person':
        if servo_2==180:
            servo_6_7=45
            servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
            RI.servo_6_7(servo_6_7)
    if servo_2!=180 and 20>time.time()-obj_found>2:
        if servo_6_7!=servo_6_7_max:
            servo_6_7=servo_6_7_max
            servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
            RI.servo_6_7(servo_6_7)           
    if follow==0:
        count_term=0
    if fetch==1 and servo_2!=0 and option_status!='person':
        if 20>time.time()-obj_found>2:
            option_status='person'
            fetch_type='person'
            servo_1_3=140
            servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
            time.sleep(2);
            servo_6_7=45
            servo_6_7=clip(servo_6_7,servo_6_7_min,servo_6_7_max)
            RI.servo_6_7(servo_6_7)
            RI.servo_1_3(servo_1_3)
    if follow==1 and count_term==0:
        #make_voice.put('cyber')
        #make_voice.put('theme')
        count_term+=1
    if glove==0:
        count_star=0
    if glove==1 and count_star==0:
        #make_voice.put('strongforce')
        make_voice.put('theforce')
        #make_voice.put('star_wars_theme')
        count_star+=1
    mqttClient.loop()
    if count_put==0:
        print('option status',option_status)
        object_to_detect.put(option_status)
        count_put+=1
    left_ultrasonic,front_top_ultrasonic,front_bottom_ultrasonic,right_ultrasonic,back_ultrasonic,roll,pitch,clamp_status=SS.read_line(left_ultrasonic,front_top_ultrasonic,front_bottom_ultrasonic,right_ultrasonic,back_ultrasonic,roll,pitch,clamp_status) #left_ultrasonic left, front_top_ultrasonic top, front_bottom_ultrasonic bottom, right_ultrasonic right, back_ultrasonic back
    try:
       
        ready_status=True
        cam.put(ready_status)
        x_AI,y_AI=rq.get(False)
        ready_status=False
        cam.put(ready_status)
        #print('x_AI: ',x_AI)
        #print('y_AI:',y_AI)
        
        if follow==1 and option_status=='person':
            if count_person==0:
                count_person=1
            move_robot(x_AI,y_AI,x_AI_old,y_AI_old)
            cum_error_x+=abs(x_AI-x_AI_old)
            avg_error_x=cum_error_x/count_person
            if avg_error_x<0.1:
                centered_on_human=True
            else:
                centered_on_human=False
            count_person+=1
        if follow==1 and option_status==fetch_type:
            count_person=0
            cum_error_x=0
            centered_on_human=False
            move_robot(x_AI,y_AI,x_AI_old,y_AI_old)
            #t_obj_y=error_new*kp_y
            phi=servo_1_3-90.0
            print('phi',phi)
            print('servo_1_3',servo_1_3)
            opp=15.*math.tan(deg_to_rad(phi)) # 15 inches for 90 degrees looking straight down
            print('opp',opp)
            if fetch==1 and aim==False and option_status!='person' and centered_on_obj==True:
                if opp<500 and opp>0:
                    t_forward=opp/30.#calibrated so that it goes half the distance
                    RI.run(100,100);time.sleep(t_forward);RI.brake();
                elif servo_1_3==90:
                    if y_AI<-0.075:
                        servo_2=180.
                        SS.servo_flashlight_laser(servo_2,flashlight,laser)
                        time.sleep(.5);
                        obj_found=time.time()
                    elif time.time()-obj_found>5:
                        RI.run(100,100);time.sleep(0.05);RI.brake();
                else:
                    pass
                
            #just_saw=False
            if (servo_1_3==100 and (x_AI>-0.05 and x_AI<0.05)) or (servo_1_3==80 and (x_AI>-0.15 and x_AI<0.15)) or (servo_1_3==180 and (x_AI>-0.15 and x_AI<0.15)):
                if abs(x_AI-x_AI_old)<0.5:
                    object_status='stationary'
                else:
                    object_status='moving'
                if front_bottom_ultrasonic<20 and servo_1_3==80:
                    pass
                else:
                    #RI.run(100,100);time.sleep(t_ball_y);RI.brake();
                    pass
                if error_new<0.1 and servo_1_3==100:
                    #servo_1_3=80
                    #RI.servo_1_3(servo_1_3);
                    pass
                if front_bottom_ultrasonic<12 and option_status==fetch_type:
                    #servo_2=180
                    #SS.servo_flashlight_laser(servo_2,flashlight,laser)
                    #time_grabbed=time.time()
                    pass
                elif error_new<0.08 and servo_1_3==80:
                    #servo_2=180
                    #SS.servo_flashlight_laser(servo_2,flashlight,laser)
                    #time_grabbed=time.time()
                    pass
                just_saw=True
                T_saw=time.time()
                
       
                    
        TI_old=time.time()
        x_AI_old=x_AI
        y_AI_old=y_AI
        
    except:
        
        count_person=0
        cum_error_x=0
        #centered_on_human=False
        t_obj=1.
        t_person=1.
        TI=time.time()
        if follow==1:
            #print('TI',TI)
            #print('TI_old',TI_old)
            #print('just_saw',just_saw)
            if (TI-T_saw>1 and TI-T_saw<30) and (option_status!='person'):
                print('exception granted')
                if y_AI_old<0:
                    servo_1_3-=y_steps;
                    servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                elif y_AI_old>0:
                    servo_1_3+=y_steps;
                    servo_1_3=clip(servo_1_3,servo_1_3_min,servo_1_3_max)
                T_saw=time.time()+.5
            if (TI-T_saw>2 and TI-T_saw<30) and (option_status=='person'):
                if x_AI_old>0:
                    RI.spin_right(100,100);time.sleep(.25);RI.brake();time.sleep(0.5)
                else:
                    RI.spin_left(100,100);time.sleep(.25);RI.brake();time.sleep(0.5)
                #T_saw=time.time()+5
            if just_saw==True and back_ultrasonic>20 and option_status==fetch_type and (time.time() -T_saw)>10:
                if time.time()-T_back>3:
                    RI.back(100,100);time.sleep(0.1);RI.brake();
                    T_back=time.time()
            if time.time()-t_reset_servos>5:
                    RI.servo_1_3(servo_1_3)
                    t_reset_servos=time.time()
            

  

        pass
 
   
    if print_ultrasonic==True:
        print("left_ultrasonic={} left, front_top_ultrasonic={} top, front_bottom_ultrasonic={} bottom, right_ultrasonic={} right, back_ultrasonic={} back".format(left_ultrasonic,front_top_ultrasonic,front_bottom_ultrasonic,right_ultrasonic,back_ultrasonic))
    if print_servo==True:
        print('servo_1_3:',servo_1_3,';   servo_2:',servo_2)
    #if servo_1_3<80:
    #    front_top_ultrasonic=front_bottom_ultrasonic

    #print('servo_1_3:',servo_1_3,'servo_6_7:',servo_6_7)
    if left_ultrasonic<40 and left_ultrasonic>10: #reads low values in error less than 10
        #print('left_ultrasonic ',left_ultrasonic)
        #print('servo_1_3:',servo_1_3,'servo_6_7:',servo_6_7)
        pass
    if front_top_ultrasonic<limit_distance and front_top_ultrasonic>0 and front_bottom_ultrasonic<limit_distance and front_bottom_ultrasonic>0 and moving_f==True:
        RI.brake()
        moving_f=False
        moving_b=False
    if front_top_ultrasonic>limit_distance:
        if follow==1:
            #if (servo_6_7==0 or servo_2!=0) and (option_status=='person'):
            if option_status=='person' and centered_on_human==True:
                RI.run(100,100)
                moving_f=True
                centered_on_human=False
            if option_status==fetch_type and centered_on_human==True:
                RI.run(100,100)
                moving_f=True
                centered_on_human=False
    else:
        if moving_f==True:
            RI.brake()
            moving_f=False
            moving_b=False
        if follow==1:
            if (servo_2!=0) and (option_status=='person') and servo_1_3!=80 and centered_on_human==True and count_person>2:
                pass

    if right_ultrasonic<40 and right_ultrasonic>0:
        pass
    if back_ultrasonic<limit_distance and back_ultrasonic>0 and moving_b==True:
        RI.brake()
        moving_f=False
        moving_b=False
    if follow==1:
        #flashlight=1
        #laser=1
        #SS.flashlight_laser(flashlight,laser)
        #SS.servo_flashlight_laser(servo_2,flashlight,laser)
        #laser=0
        #flashlight=0
        #SS.flashlight_laser(flashlight,laser)
        #SS.servo_flashlight_laser(servo_2,flashlight,laser)
        pass
    if glove==1:
        if roll>45:
            RI.run(100,100);
            moving_f=True
        elif roll<-45:
            RI.back(100,100);
            moving_b=True
        else:
            RI.brake();
            moving_f=False
            moving_b=False
        if pitch>45:
             RI.spin_right(100,100);
        elif pitch<-45:
            RI.spin_left(100,100);
        elif moving_f==False and moving_b==False:
            RI.brake();
        else:
            pass
        if clamp_status==1:
            if servo_2==0:
                make_voice.put('strongforce')
                make_voice.put('light_on')
            servo_2=180
            SS.servo_flashlight_laser(servo_2,flashlight,laser)
        elif clamp_status==0:
            if servo_2==180:
                make_voice.put('light_off')
            servo_2=0
            SS.servo_flashlight_laser(servo_2,flashlight,laser)
        else:
            pass
        
    else:
        pass
            



