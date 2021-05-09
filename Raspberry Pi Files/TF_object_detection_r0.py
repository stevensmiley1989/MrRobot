import io
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tflite_runtime.interpreter import Interpreter
from tensorflow.lite.python import interpreter as ip
import datetime
global img
from multiprocessing import Process, Queue, Pipe
pi=Queue()
w=Queue()
cam=Queue()
from threading import Thread
import importlib.util
import os
from collections import deque
import imutils
import time
from multiprocessing import Process, Queue

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
def folder_path(path):
    try:
        os.mkdir(path)
    except OSError:
        return(path)
    else:
        return(path)
    return(path)
currentDirectory=os.getcwd()
print(currentDirectory)
case=2 #initial case to run
global case1,case2,case3
case1=False
case2=False
case3=False
def case_run(case):
    global path_output,label_path,default_model,detected_item,option_status,model_path,thresh,case1,case2,case3
    if case==1:   
        path_output="/home/pi/Desktop/Output/Ball_Pictures/Orange_Ball/"
        
        thresh=0.35
        label_path='./models/orange_ball_labels.txt'
        model_path='./models/'
        default_model='model-9.tflite'
        detected_item='orange_ball'
        option_status='orange_ball'
        mkdir('Output')
        mkdir('Output/Ball_Pictures')
        if case1==False:
            print('Case 1: Orange Ball Detection selected')
            case1=True
            case2=False
            case3=False
            try:
                os.mkdir(path_output)
            except:
                pass
    if case==2:
        path_output="/home/pi/Desktop/Output/Toy_Pictures/reindeer/"
        label_path='./models/reindeer_labels.txt'
        model_path='./models/'
        #default_model='model_toy-5.tflite'
        #default_model='ssd_MobileNet_v2FPNLite_320_LR0p001_BS32_NB30000_5_2_2021_reindeer_model_toy.tflite'
        #default_model='ssd_MobileNet_v2FPNLite_320_LR0p001_BS32_NB50000_5_2_2021_reindeer_model_toy.tflite'
        default_model='augmented_ssd_MobileNet_v2FPNLite_320_LR0p001_BS32_NB70000_5_5_2021_reindeer_model_toy.tflite'
        #default_model='ssd_MobileNet_v2FPNLite_320_LR0p001_BS32_NB70000_5_5_2021_reindeer_model_toy-2.tflite'
        #default_model='augmented_ssd_MobileNet_v2FPNLite_320_LR0p001_BS32_NB70000_5_5_2021_reindeer_model_toy.tflite'
        #default_model='ssd_MobileNet_v2FPNLite_640_LR0p001_BS32_NB10000_4_30_2021_reindeer_model_toy.tflite'
        thresh=0.5
        detected_item='reindeer'
        option_status='reindeer'
        mkdir('Output')
        mkdir('Output/Toy_Pictures')
        if case2==False:
            print('Case 2: Reindeer Detection selected')
            case1=False
            case2=True
            case3=False
            try:
                os.mkdir(path_output)
            except:
                pass
    if case==3:
        path_output="/home/pi/Desktop/Output/People/Steven/"
        label_path = './models/coco_labels.txt'
        model_path='./models/'
        default_model='detect.tflite'
        thresh=0.5
        detected_item='person'
        option_status='person'
        mkdir('Output')
        mkdir('Output/Person')
        if case3==False:
            print('Case 3: Person Detection selected')
            case1=False
            case2=False
            case3=True
            try:
                os.mkdir(path_output)
            except:
                pass

case_run(case)
follow=1
global WIDTH, HEIGHT
WIDTH,HEIGHT = 640,480

pic_status="Picture_Off"






# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(WIDTH,HEIGHT),framerate=40):#use to be 30
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0) 
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True

FONT = cv2.FONT_HERSHEY_SIMPLEX
COLORS = np.random.uniform(0, 255, size=(90, 3))
def detectObjImg(img_path):

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = cv2.resize(img, (width, height), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
    results = detect_objects(interpreter, image, 0.4)
    
    id = int(results[0]['class_id'])
    prob = int(round(results[0]['score'], 2)*100)
    
    HEIGHT, WIDTH, _ = img.shape
    ymin, xmin, ymax, xmax = results[0]['bounding_box']
    xmin = int(xmin * WIDTH)
    xmax = int(xmax * WIDTH)
    ymin = int(ymin * HEIGHT)
    ymax = int(ymax * HEIGHT)
    
    scale = HEIGHT/600
    ln = int(6*scale)
    hf = int(ln/3)

    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), ln, 3 )
    img = cv2.putText(img, labels[id], (xmin+ln, ymin+7*ln), font, hf, (0, 0, 255), ln)
    img = cv2.putText(img, str(prob)+"%", (xmin+ln, ymax-ln), font, hf, (0, 0, 255), ln)
    plt.figure(figsize=(15,8))
    plt.imshow(img)
    plt.axis('off');
ready_status=True
def detect_mult_object_picture(img, results,w,cam,detected_item):
    global m1, t1, m2, t2,ready_status
    
    H, W, _ = img.shape
    aspect = W/H
    #WIDTH =640
    H = int(WIDTH/aspect)#int(640/aspect)
    dim = (W, H)
    
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    i=0
    prob_i=0
    for j in range(len(results)):
        id = int(results[j]['class_id'])
        if labels[id].find(detected_item)==-1:
            return img
        elif labels[id]==detected_item:
            dummy=int(round(results[j]['score'],2)*100)
            if dummy>prob_i:
                i=j
                prob_i=dummy
        else:
            pass
        
    if results:#for i in range(len(results)):
        id = int(results[i]['class_id'])
        prob = int(round(results[i]['score'], 2)*100)
        
        ymin, xmin, ymax, xmax = results[i]['bounding_box']
        #print('xmin',xmin,' xmax',xmax, ' ymin',ymin,' ymax',ymax)
        
        xcent=round((xmin+xmax)/2.0,2)
        ycent=round((ymin+ymax)/2.0,2)
        xmin = int(xmin * W)
        xmax = int(xmax * W)
        ymin = int(ymin * H)
        ymax = int(ymax * H)
        
        
        if labels[id].find(detected_item)==-1:
            return img
        else:
            text="{}: {}% ".format(detected_item,prob)          
            ready_status=cam.get()
            if follow==1 and i==0 and ready_status==True:
                xcent=round(-1.*(xcent-0.5),3)
                ycent=round(-1.*(ycent-0.5),3)
                print('x:  ',xcent)
                print('y:  ',ycent)
                t2=time.time()
                w.put((xcent,ycent))
                text = "{}: {}%, xcent = {}, ycent = {}".format(labels[id], prob,xcent,ycent)
                m2=xcent
        if ymin > 10: ytxt = ymin-10
        else: ytxt = ymin+15
       
        img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), COLORS[id], thickness=2)
        img = cv2.putText(img, text, (xmin+3, ytxt), FONT, 0.5, COLORS[id], 2)

    return img
def detect_mult_object_picture2(img, results,detected_item):
    global m1, t1, m2, t2,ready_status
    ready_status=True
    
    H, W, _ = img.shape
    aspect = W/H
    #WIDTH =640
    H = int(WIDTH/aspect)#int(640/aspect)
    dim = (W, H)
    
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     
    for i in range(len(results)):
        id = int(results[i]['class_id'])
        prob = int(round(results[i]['score'], 2)*100)
        
        ymin, xmin, ymax, xmax = results[i]['bounding_box']
        xcent=round((xmin+xmax)/2.0,2)
        ycent=round((ymin+ymax)/2.0,2)
        xmin = int(xmin * W)
        xmax = int(xmax * W)
        ymin = int(ymin * H)
        ymax = int(ymax * H)
        
        text = "{}: {}%".format(labels[id], prob)

        if labels[id].find(detected_item)==-1:
            return img
        else:
            text="{}: {}% ".format(detected_item,prob)
            try:
                read_status=True
            except:
                ready_status=False
            if follow==1 and i==0 and ready_status==True:
                xcent=round(-1.*(xcent-0.5),2)
                ycent=round(-1.*(ycent-0.5),2)
                print('x:  ',xcent)
                print('y:  ',ycent)
                t2=time.time()
                m2=xcent
                if ymin > 10: ytxt = ymin-10
                else: ytxt = ymin+15
                img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), COLORS[id], thickness=2)
                img = cv2.putText(img, text, (xmin+3, ytxt), FONT, 0.5, COLORS[id], 2)
                break
        
       


    return img
def load_labels(path):
    """Loads the labels file. Supports files with or without index numbers."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        labels = {}

        for row_number, content in enumerate(lines):
            pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
            if len(pair) == 2 and pair[0].strip().isdigit():
                labels[int(pair[0])] = pair[1].strip()
            else:
                labels[row_number] = pair[0].strip()
        return labels


def set_input_tensor(interpreter, image):
    """Sets the input tensor."""
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
    """Returns the output tensor at the given index."""
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    return tensor    


def detect_objects(interpreter, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()

    # Get all output details
    boxes = get_output_tensor(interpreter, 0)
    classes = get_output_tensor(interpreter, 1)
    scores = get_output_tensor(interpreter, 2)
    count = int(get_output_tensor(interpreter, 3))

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
              'bounding_box': boxes[i],
              'class_id': classes[i],
              'score': scores[i]
            }
            results.append(result)
    return results



labels = load_labels(label_path)
image_path = folder_path(currentDirectory+'/images')
import argparse
import importlib.util
parser = argparse.ArgumentParser()
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default=default_model)#default_model detect.tflite
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

use_TPU = args.edgetpu   
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime import interpreter as ip
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
        print('using TPU')
else:
    from tensorflow.lite.python import interpreter as ip
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate
PATH_TO_CKPT=os.path.join(model_path,default_model)
if use_TPU:
    interpreter = ip.Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = ip.Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']

def init(pi,w,cam,object_to_detect,pic):
    global labels,pic_status
    cap = VideoStream().start()
    RI_Out_In='OUT'
    RI_Out_In='IN'
    global m1,m2,t1,t2
    t1=time.time()
    m1=0.
    t2=t1
    m2=m1
    t_picture=t1
    global img
    count_i=0
    while True:
        try:
            pic_status_new=pic.get(False)
            pic_status=pic_status_new
        except:
            pic_status=pic_status
        try:
            option_status_new=object_to_detect.get(False)
            option_status=option_status_new
        except:
            option_status=option_status
        if option_status=='ball':
            case=1
            #label_path='./models/orange_ball_labels.txt'
            #model_path='./models/'
            #default_model='model-10.tflite'
            #detected_item='orange_ball'
            case_run(case)
        if option_status=='reindeer':
            case=2
            #label_path='./models/reindeer_labels.txt'
            #model_path='./models/'
            #default_model='model_toy-5.tflite'
            #detected_item='reindeer'
            case_run(case)
        if option_status=='person':
            case=3
            #label_path = './models/coco_labels.txt'
            #model_path='./models/'
            #default_model='detect.tflite'
            #detected_item='person'
            case_run(case)
        labels = load_labels(label_path)  
        from tflite_runtime.interpreter import Interpreter
        from tensorflow.lite.python import interpreter as ip
        parser = argparse.ArgumentParser()
        parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                            default=default_model)#default_model detect.tflite
        parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                            action='store_true')

        args = parser.parse_args()

        use_TPU = args.edgetpu   
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime import interpreter as ip
            if use_TPU:
                from tflite_runtime.interpreter import load_delegate
                print('using TPU')
        else:
            from tensorflow.lite.python import interpreter as ip
            if use_TPU:
                from tensorflow.lite.python.interpreter import load_delegate
        PATH_TO_CKPT=os.path.join(model_path,default_model)
        if use_TPU:
            interpreter = ip.Interpreter(model_path=PATH_TO_CKPT,
                                      experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            print(PATH_TO_CKPT)
        else:
            interpreter = ip.Interpreter(model_path=PATH_TO_CKPT)
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
        
        t1=time.time()
        timer = cv2.getTickCount()
        img=cap.read()
        img = cv2.flip(img,-1)
        img = cv2.flip(img,1)

        if RI_Out_In=='OUT':
            img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
        elif RI_Out_In=='IN':
            pass
        image=img
        img_og=img

        image = cv2.resize(image, (width, height), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)

        start_time = time.time()
        if detected_item=='person':
            image=image
            #thresh=0.5
        if detected_item=='orange_ball':
            image_og=image
            image=image/255
            #thresh=0.35
        if detected_item=='reindeer':
            image_og=image
            image=image/255
            #thresh=0.55

        results = detect_objects(interpreter, image, thresh)
        elapsed_ms = (time.time() - start_time) * 1000
        ti=str(datetime.datetime.now()).replace(' ','_').replace(':','c').replace('.','p')
        #if time.time() - t_picture>30:
        try:
            os.mkdir(path_output+'{}x{}/'.format(str(height),str(width)))
        except:
            pass
        if pic_status=="Picture_1" or pic_status=="Picture_On":
            if detected_item!='person':
                cv2.imwrite(path_output+'{}x{}/'.format(str(height),str(width))+"{}_{}.jpg".format(count_i,ti),image_og)
            else:
                cv2.imwrite(path_output+'{}x{}/'.format(str(height),str(width))+"{}_{}.jpg".format(count_i,ti),image)
            t_picture=time.time()
            if pic_status=="Picture_1":
                pic_status="Picture_Off"
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        #cv2.putText(img, "FPS: "+str(int(fps)), (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        if option_status=='person':
            img = detect_mult_object_picture(img, results,w,cam,detected_item)
        if option_status=='ball':
            img = detect_mult_object_picture(img,results,w,cam,detected_item)
        if option_status=='reindeer':
            img = detect_mult_object_picture(img,results,w,cam,detected_item)
        #print('detecting ball from TF_app_copy')
        cv2.imshow("MrRobot_r0", img)
        if pic_status=="Picture_1" or pic_status=="Picture_On":
            try:
                os.mkdir('Output_Video')
            except:
                pass
            video_path_output='Output_Video/'
            if detected_item!='person':
                cv2.imwrite(video_path_output+"{:0>4d}_{}.jpg".format(count_i,ti),img)
            else:
                cv2.imwrite(video_path_output+"{:0>4d}_{}.jpg".format(count_i,ti),img)
            t_picture=time.time()
            if pic_status=="Picture_1":
                pic_status="Picture_Off"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count_i+=1
    cap.stop()
    cv2.destroyAllWindows()

    plt.figure(figsize=(15,8))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off');

def init2():
    # This is similar to init1, but is made for a standalone test
    # without needing to pass parallel processed Queue variables
    global m1,m2,t1,t2
    global img
    cap = VideoStream().start()
    RI_Out_In='IN'   
    t1=time.time()
    m1=0.
    t2=t1
    m2=m1    
    while True:
        from tflite_runtime.interpreter import Interpreter
        from tensorflow.lite.python import interpreter as ip
        parser = argparse.ArgumentParser()
        parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                            default=default_model)#default_model detect.tflite
        parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                            action='store_true')

        args = parser.parse_args()

        use_TPU = args.edgetpu   
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime import interpreter as ip
            if use_TPU:
                from tflite_runtime.interpreter import load_delegate
                print('using TPU')
        else:
            from tensorflow.lite.python import interpreter as ip
            if use_TPU:
                from tensorflow.lite.python.interpreter import load_delegate
        PATH_TO_CKPT=os.path.join(model_path,default_model)
        if use_TPU:
            interpreter = ip.Interpreter(model_path=PATH_TO_CKPT,
                                      experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            print(PATH_TO_CKPT)
        else:
            interpreter = ip.Interpreter(model_path=PATH_TO_CKPT)
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
     
        t1=time.time()
        timer = cv2.getTickCount()
        #success, img = cap.read()
        img=cap.read()
            

        img = cv2.flip(img,-1)
        img = cv2.flip(img,1)
        #img=cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        if RI_Out_In=='OUT':
            img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
        elif RI_Out_In=='IN':
            pass
        img_og=img
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        #cv2.putText(img, "FPS: "+str(int(fps)), (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        
        #image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image=img
        image = cv2.resize(image, (width, height), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
        start_time = time.time()
        if detected_item=='person':
            image=image
            thresh=0.5
        if detected_item=='reindeer':
            image=image/255
            thresh=0.6
        results = detect_objects(interpreter, image, thresh)
        elapsed_ms = (time.time() - start_time) * 1000
        
        img = detect_mult_object_picture2(img, results,detected_item)
        cv2.imshow("Smiley's Machine Learning Image Analysis ==> Press [q] to Exit", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.stop()
    cv2.destroyAllWindows() 
    plt.figure(figsize=(15,8))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off');
 
