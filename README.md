# MrRobot
## Repository by Steven Smiley

This respository hosts the files I used to create my DIY robot, MrRobot.
![MrRobot_r0](https://github.com/stevensmiley1989/MrRobot/blob/main/Images/MrRobot_FusionvsReal.png)
# Table of Contents to Repository
* [0. Diagrams](#0)
   * [0.1 Wiring Diagram](#0.1)
   * [0.2 Training Flowchart](#0.2)
* [1. Jupyter Notebooks](#1)
* [2. Adruino Codes](#2)
* [3. Python Codes](#3)
* [4. Autodesk Fusion360 File](#4)
* [5. iOS Application](#5)
* [6. Images](#6)
* [7. Credits/References](#7)
* [8. Contact-Info](#8)
* [9. License](#9)

## 0. Diagrams<a class="anchor" id="0"></a>
### 0.1 Wiring Diagram<a class="anchor" id="0.1"></a>
![Wiring Diagram](https://github.com/stevensmiley1989/MrRobot/blob/main/Images/MrRobot_Wiring_Diagram.png)
### 0.2 Training Flowchart<a class="anchor" id="0.2"></a>
![Training Flowchart](https://github.com/stevensmiley1989/MrRobot/blob/main/Images/MrRobot_Training_Flowchart.png)

## 1. Jupyter Notebooks<a class="anchor" id="1"></a>
Jupyter Notebook(s) written in Python.

| Notebook | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Grab_from_Gdrive.ipynb](https://nbviewer.jupyter.org/github/stevensmiley1989/MrRobot/blob/main/Grab_from_Gdrive.ipynb) | Pipeline Images from Gdrive to Local Machine for LabelImg to put Bounding Boxes and send back to Gdrive for training on Google Colab. |
| [augmented_ssd_MobileNet_v2_FPNLite_320x320_5_8_2021_reindeer.ipynb](https://nbviewer.jupyter.org/github/stevensmiley1989/MrRobot/blob/main/Jupyter%20Notebooks/augmented_ssd_MobileNet_v2_FPNLite_320x320_5_8_2021_reindeer.ipynb) | Training notebook for Object Detector with SSD MobileNet V2 FPNLite 320x320 on Google Colab. |
| [Evaluate_Models.ipynb](https://nbviewer.jupyter.org/github/stevensmiley1989/MrRobot/blob/main/Jupyter%20Notebooks/Evaluate_Models.ipynb) | Evaluation notebook for Object Detector with SSD MobileNet V2 FPNLite 320x320 on Google Colab. |

## 2. Arduino Codes<a class="anchor" id="2"></a>
Arduino Code(s) written in C++/C.

| Code | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [MrRobot_Receiver_Slave_Arduino_1.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/Arduino%20Codes/MrRobot_Receiver_Slave_Arduino_1.ino) | Arduino 1, Receiver Slave. |
| [MrRobot_Receiver_Master_Arduino_2_with_coil.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/Arduino%20Codes/MrRobot_Receiver_Master_Arduino_2_with_coil.ino) | Arduino 2, Master.  This is Arduino controls the other slaves and is connected via Serial to the Raspberry Pi with USB.  |
| [MrRobot_Transmitter_Arduino_3.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/Arduino%20Codes/MrRobot_Transmitter_Arduino_3.ino) | Arduino 3, Transmitter.  This is for the glove that can control the robot using the MPU06050 and FlexSensor. |
| [MrRobot_Receiver_Slave_Arduino_4_with_coil.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/Arduino%20Codes/MrRobot_Receiver_Slave_Arduino_4_with_coil.ino) | Arduino 4, Receiver Slave.  This Arduino opens and closes the relays to the coil gun after receiving the signal from the Master for charging, stepping, or firing. |

## 3. Python Codes<a class="anchor" id="3"></a>
Python Code(s) written in Python.

| Code | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [PI-app_r0.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/PI-app_r0.py) | Main script controlling the robot.  This is the file initiated to start the robot.  |
| [Robot_Integrate_r0.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/Robot_Integrate_r0.py) | This script controls the DC motors for the wheels and the Servo motors for the gripper and coil arms.  It is executed during the PI-app_r0.py execution.|
| [Send_to_Gdrive.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/Send_to_Gdrive.py) | This script sends the images taken from the robot to the Gdrive as part of the training process.  |
| [Serial_Connect_Stepper_r0.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/Serial_Connect_Stepper_r0.py) | This script receives and transmits serial communication to the Arduinos.  It is executed during the PI-app_r0.py execution.  |
| [TF_object_detection_r0.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/TF_object_detection_r0.py) | This script runs inference with the tflite model using the Edge Coral TPU and is run in parallel with PI-app_r0.py for controlling the robot.  It is executed during the PI-app_r0.py execution.  |
| [play_sound_r0.py](https://github.com/stevensmiley1989/MrRobot/blob/main/Raspberry%20Pi%20Files/play_sound_r0.py) | This script plays soundboard clips at various times in the robot's activity.  It is executed during the PI-app_r0.py execution.  |

## 4. Autodesk Fusion 360 File<a class="anchor" id="4"></a>
Created in Autodesk Fusion 360.

| File | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [MrRobot_r0.f3d](https://github.com/stevensmiley1989/MrRobot/blob/main/Autodesk%20Fusion360%20File/MrRobot_r0.f3d) | Fusion360 file for MrRobot_r0. |

![Fusion360 Screenshot](https://github.com/stevensmiley1989/MrRobot/blob/main/Images/MrRobot_Fusion360_Screenshot.png)

## 5. iOS Application<a class="anchor" id="5"></a>
Created in Xcode with Swift.

| File | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [MyRobot](https://github.com/stevensmiley1989/MrRobot/tree/main/iOS_Application/MyRobot) | iOS Application for MrRobot_r0. |

![iPhone App](https://github.com/stevensmiley1989/MrRobot/blob/main/Images/MrRobot_r0_Xcode_Screenshot.png)

## 6. Images<a class="anchor" id="6"></a>
[Images used for this Repository.](https://github.com/stevensmiley1989/MrRobot/tree/main/Images)

## 7. Credits/References<a class="anchor" id="7"></a>
1. TensorFlow 2 Detection Model Zoo, [https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md]<a class="anchor" id="Ref_1"></a>  

2. SSD MobilNet V2 FPNLite 320x320, [http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz] <a class="anchor" id="Ref_2"></a>   

3. Liu, Wei et al. "SSD: Single Shot MultiBox Detector" [https://arxiv.org/abs/1512.02325] <a class="anchor" id="Ref_3"></a>   

4. TensorFlow.  Martín Abadi, Ashish Agarwal, Paul Barham, Eugene Brevdo, Zhifeng Chen, Craig Citro, Greg S. Corrado, Andy Davis,Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Ian Goodfellow, Andrew Harp, Geoffrey Irving, Michael Isard, Rafal Jozefowicz, Yangqing Jia,Lukasz Kaiser, Manjunath Kudlur, Josh Levenberg, Dan Mané, Mike Schuster,Rajat Monga, Sherry Moore, Derek Murray, Chris Olah, Jonathon Shlens,Benoit Steiner, Ilya Sutskever, Kunal Talwar, Paul Tucker,Vincent Vanhoucke, Vijay Vasudevan, Fernanda Viégas,Oriol Vinyals, Pete Warden, Martin Wattenberg, Martin Wicke,Yuan Yu, and Xiaoqiang Zheng.  TensorFlow: Large-scale machine learning on heterogeneous systems, 2015. Software available from tensorflow.org. <a class="anchor" id="Ref_4"></a>   

5. LabelImg. [https://github.com/tzutalin/labelImg] <a class="anchor" id="Ref_5"></a>   

6. Bradski, G., & Kaehler, A. (2008). Learning OpenCV: Computer vision with the OpenCV library. " O&#x27;Reilly Media, Inc." <a class="anchor" id="Ref_6"></a>   

7.  SciPy. Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, Stéfan J. van der Walt, Matthew Brett, Joshua Wilson, K. Jarrod Millman, Nikolay Mayorov, Andrew R. J. Nelson, Eric Jones, Robert Kern, Eric Larson, CJ Carey, İlhan Polat, Yu Feng, Eric W. Moore, Jake VanderPlas, Denis Laxalde, Josef Perktold, Robert Cimrman, Ian Henriksen, E.A. Quintero, Charles R Harris, Anne M. Archibald, Antônio H. Ribeiro, Fabian Pedregosa, Paul van Mulbregt, and SciPy 1.0 Contributors. (2019) SciPy 1.0–Fundamental Algorithms for Scientific Computing in Python. preprint arXiv:1907.10121 <a class="anchor" id="Ref_7"></a>   

8.  Python. a) Travis E. Oliphant. Python for Scientific Computing, Computing in Science & Engineering, 9, 10–20 (2007) b) K. Jarrod Millman and Michael Aivazis. Python for Scientists and Engineers, Computing in Science & Engineering, 13, 9–12 (2011) <a class="anchor" id="Ref_8"></a>   

9.  NumPy. a) Travis E. Oliphant. A guide to NumPy, USA: Trelgol Publishing, (2006). b) Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux. The NumPy Array: A Structure for Efficient Numerical Computation, Computing in Science & Engineering, 13, 22–30 (2011) <a class="anchor" id="Ref_9"></a>   

10.  IPython. a) Fernando Pérez and Brian E. Granger. IPython: A System for Interactive Scientific Computing, Computing in Science & Engineering, 9, 21–29 (2007) <a class="anchor" id="Ref_10"></a>   

11.  Matplotlib. J. D. Hunter, “Matplotlib: A 2D Graphics Environment”, Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, 2007. <a class="anchor" id="Ref_11"></a>   

12.  Pandas. Wes McKinney. Data Structures for Statistical Computing in Python, Proceedings of the 9th Python in Science Conference, 51–56 (2010) <a class="anchor" id="Ref_12"></a>   

13. Scikit-Learn. Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vincent Dubourg, Jake Vanderplas, Alexandre Passos, David Cournapeau, Matthieu Brucher, Matthieu Perrot, Édouard Duchesnay. Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research, 12, 2825–2830 (2011) <a class="anchor" id="Ref_13"></a>   

14.  Scikit-Image. Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image contributors. scikit-image: Image processing in Python, PeerJ 2:e453 (2014) <a class="anchor" id="Ref_14"></a>   

15.  Coral USB Accelerator. [https://coral.ai/products/accelerator/] <a class="anchor" id="Ref_15"></a>  

16.  MrRobot GitHub Repo. [https://github.com/stevensmiley1989/MrRobot]<a class="anchor" id="Ref_16"></a> 

17.  Raspberry Pi Guide - MQTT Protocol. [https://www.raspberrypi.org/forums/viewtopic.php?t=196010]<a class="anchor" id="Ref_17"></a> 

18.  Rclone Guide. [https://rclone.org/drive/]<a class="anchor" id="Ref_18"></a> 

19.  How to Control the Speed and Stability of Training Neural Networks with Gradient Descent Batch Size. [https://machinelearningmastery.com/how-to-control-the-speed-and-stability-of-training-neural-networks-with-gradient-descent-batch-size/]<a class="anchor" id="Ref_19"></a> 

20.  Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, Liang-Chieh Chen, MobileNetV2: Inverted Residuals and Linear Bottlenecks.[https://arxiv.org/abs/1801.04381]<a class="anchor" id="Ref_20"></a> 

21.  Cheng, Shuhong & Zhao, Kaopeng & Zhang, Dianfan. (2019). Abnormal Water Quality Monitoring Based on Visual Sensing of Three-Dimensional Motion Behavior of Fish. Symmetry. 11. 1179. 10.3390/sym11091179.<a class="anchor" id="Ref_21"></a> 

## 8. Contact-Info<a class="anchor" id="8"></a>

Feel free to contact me to discuss any issues, questions, or comments.

* Email: [stevensmiley1989@gmail.com](mailto:stevensmiley1989@gmail.com)
* GitHub: [stevensmiley1989](https://github.com/stevensmiley1989)
* LinkedIn: [stevensmiley1989](https://www.linkedin.com/in/stevensmiley1989)
* Kaggle: [stevensmiley](https://www.kaggle.com/stevensmiley)

### 9. License <a class="anchor" id="9"></a>

This repository contains a variety of content; some developed by Steven Smiley, and some from third-parties.  The third-party content is distributed under the license provided by those parties.

The content developed by Steven Smiley is distributed under the following license:

*I am providing code and resources in this repository to you under an open source license.  Because this is my personal repository, the license you receive to my code and resources is from me and not my employer. 

   Copyright 2021 Steven Smiley
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
