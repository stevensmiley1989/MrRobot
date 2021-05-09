import serial
import time
import datetime
import os


os.system('ls /dev/Arduino_Nano_1 >ff.txt')
f=open('ff.txt','r')
f_read=f.readlines()
f.close()
os.system('rm ff.txt')
global fs,ls,rs
#ser.write("stepper10;\n".encode())
#ser.write("flashlight1;\n".encode('ascii'))
for line in f_read:
    try:
        line=line.strip()
        ser=serial.Serial(line,115200,timeout=5) #change ACM number as found from ls /dev/tty/ACM*
        #print(ser) 
        break
    except:
        pass
ser.baudrate=115200
def enc(message):
    ser.write(message.encode())
    print(message,' sent')

        
    
def step_to(x): #-360 to 360, typically 0 front and center, 50 is 90 degrees, -50 is -90 degrees
    step_write=str(x)
    step_write='stepper'+step_write.strip()+';\n'
    enc(step_write)
def servo_to(x): #-360 to 360, typically 0 front and center, 50 is 90 degrees, -50 is -90 degrees
    servo_write=str(x)
    servo_write='servo'+servo_write.strip()+';\n'
    enc(servo_write)

def flashlight_laser(x,y): #1 or 0
    step_write='flashlight{} laser{};\n'.format(x,y)
    enc(step_write)
def servo_flashlight_laser(w,x,y): #1 or 0
    s_write=str(w)
    sfl_write='servo'+s_write.strip()+'flashlight{} laser{};\n'.format(x,y)
    enc(sfl_write)
def step_to(): #1 or 0
    sfl_write='step_to laser1;\n'
    enc(sfl_write)
def reset(): #1 or 0
    sfl_write='reset laser1;\n'
    enc(sfl_write)
def on6(): #1 or 0
    sfl_write='on6 laser1;\n'
    enc(sfl_write)
def charge(): #1 or 0
    sfl_write='charge laser1;\n'
    enc(sfl_write)
def trigger(): #1 or 0
    sfl_write='trigger laser1;\n'
    enc(sfl_write)

global s0, s1, s2, s3,s4
s0=120
s1=120
s2=120
s3=120
s4=120
global roll, pitch, clamp_status
roll=0
pitch=0
clamp_status=0
def read_line(s0,s1,s2,s3,s4,roll,pitch,clamp_status):
    nrf=False
    i=0
    while nrf==False and i<5:
#    for i in range(0,10):
        try:
            ser=serial.Serial(line,115200,timeout=5) #change ACM number as found from ls /dev/tty/ACM*
            ser.flush()
            data_og=ser.readline()
            data_og=data_og.decode("utf-8").strip()
            #print(data)
            ser.flush()
            if data_og.find("Roll:")==-1:
                data=data_og.replace(';','')
                s0_s=data.split("\t")[0].strip() #s0
                s1_s=data.split("\t")[1].strip() #s1
                s2_s=data.split("\t")[2].strip() #s2
                s3_s=data.split("\t")[3].strip() #s3
                s4_s=data.split("\t")[4].strip() #s4
                if s0_s and s1_s and s2_s and s3_s and s4_s:
                    if(int(s0_s))>0:
                        s0=(int(s0_s)+s0)/2.
                    s0=int(s0)
                    if(int(s1_s))>0:
                        s1=(int(s1_s)+s1)/2.
                    s1=int(s1)
                    if(int(s2_s))>0:
                        s2=(int(s2_s)+s2)/2.
                    s2=int(s2)
                    if(int(s3_s))>0:
                        s3=(int(s3_s)+s3)/2.
                    s3=int(s3)
                    if(int(s4_s))>0:
                        s4=(int(s4_s)+s4)/2.
                    s4=int(s4)
            else:
                data=data_og               
                roll_s=data.split("Roll:")[1].split(";")[0].strip() #roll
                pitch_s=data.split("Pitch:")[1].split(";")[0].strip() #pitch
                clamp_status_s=data.split("clamp_status:")[1].split(";")[0].strip() #clamp_status
                #print(data)
                if roll_s and pitch_s and clamp_status_s:
                    roll=int(float(roll_s))+11
                    pitch=int(float(pitch_s))-22
                    clamp_status=int(float(clamp_status_s))
                nrf=True
                break
            
        except:
            #print()
            pass
        i+=1
    #print(s0,s1,s2,s3,roll,pitch,clamp_status)
    return s0,s1,s2,s3,s4,roll,pitch,clamp_status
    
        
def test(s0=s0,s1=s1,s2=s2,s3=s3,s4=s4,roll=roll,pitch=pitch,clamp_status=clamp_status):
    while True:
        s0,s1,s2,s3,s4,roll,pitch,clamp_status=read_line(s0,s1,s2,s3,s4,roll,pitch,clamp_status)
        print(s0,s1,s2,s3,s4,roll,pitch,clamp_status)
