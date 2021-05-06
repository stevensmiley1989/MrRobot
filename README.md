# MrRobot
## Repository by Steven Smiley

This respository hosts the files I used to create my DIY robot, MrRobot.

# Table of Contents to Repository 
* [1. Jupyter Notebooks](#1)
* [2. Adruino Codes](#2)
* [3. Python Codes](#3)
* [2. Inputs](#2)
   * [data.csv](#2)
* [3. Outputs](#3)
   * [Models](#3.1)
   * [Figures](#3.2)
* [4. Credits/References](#4)
* [5. Contact-Info](#5)
* [6. License](#6)

## 1 Jupyter Notebooks<a class="anchor" id="1"></a>
Jupyter Notebook(s) written in Python.

| Notebook | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Grab_from_Gdrive.ipynb](https://nbviewer.jupyter.org/github/stevensmiley1989/MrRobot/blob/main/Grab_from_Gdrive.ipynb) | Pipieline Images from Gdrive to Local Machine for LabelImg to put Bounding Boxes and send back to Gdrive for training on Google Colab. |
| [augmented_ssd_MobileNet_v2_FPNLite_320_LR0p01_BS32_NB80000__5_5_2021_reindeer.ipynb](https://nbviewer.jupyter.org/github/stevensmiley1989/MrRobot/blob/main/augmented_ssd_MobileNet_v2_FPNLite_320_LR0p01_BS32_NB80000__5_5_2021_reindeer.ipynb) | Training notebook for Object Detector with SSD MobileNet V2 FPNLite 320x320 on Google Colab. |

## 2 Arduino Codes<a class="anchor" id="2"></a>
Arduino Code(s) written in C++/C.

| Code | Description |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [MrRobot_Receiver_Slave_Arduino_1.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/MrRobot_Receiver_Slave_Arduino_1.ino) | Arduino 1, Receiver Slave. |
| [MrRobot_Receiver_Master_Arduino_2_with_coil.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/MrRobot_Receiver_Master_Arduino_2_with_coil.ino) | Arduino 2, Master.  This is Arduino controls the other slaves and is connected via Serial to the Raspberry Pi with USB.  |
| [MrRobot_Transmitter_Arduino_3.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/MrRobot_Transmitter_Arduino_3.ino) | Arduino 3, Transmitter.  This is for the glove that can control the robot using the MPU06050 and FlexSensor. |
| [MMrRobot_Receiver_Slave_Arduino_4_with_coil.ino](https://github.com/stevensmiley1989/MrRobot/blob/main/MrRobot_Receiver_Slave_Arduino_4_with_coil.ino) | Arduino 4, Receiver Slave.  This Arduino opens and closes the relays to the coil gun after receiving the signal from the Master for charging, stepping, or firing. |


## 4 Contact-Info<a class="anchor" id="5"></a>

Feel free to contact me to discuss any issues, questions, or comments.

* Email: [stevensmiley1989@gmail.com](mailto:stevensmiley1989@gmail.com)
* GitHub: [stevensmiley1989](https://github.com/stevensmiley1989)
* LinkedIn: [stevensmiley1989](https://www.linkedin.com/in/stevensmiley1989)
* Kaggle: [stevensmiley](https://www.kaggle.com/stevensmiley)

### 6 License <a class="anchor" id="6"></a>

This repository contains a variety of content; some developed by Steven Smiley, and some from third-parties.  The third-party content is distributed under the license provided by those parties.

The content developed by Steven Smiley is distributed under the following license:

*I am providing code and resources in this repository to you under an open source license.  Because this is my personal repository, the license you receive to my code and resources is from me and not my employer. 

   Copyright 2021 Steven Smiley

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
