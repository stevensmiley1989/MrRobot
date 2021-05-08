//
//  ViewController.swift
//  MyRobot
//
//  Created by Steven Smiley on 1/31/21.
//

import UIKit
import CocoaMQTT

class ViewController: UIViewController {
    let mqttClient = CocoaMQTT(clientID: "pi3", host: "192.168.1.30", port: 1883)

    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func connectButton(_ sender: UIButton) {
        mqttClient.connect()
    }
    
    @IBAction func disconnectButton(_ sender: UIButton) {
        mqttClient.disconnect()
    }
    @IBAction func case1(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio", withString: "case1")
    }
    @IBAction func case2(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio", withString: "case2")
    }
    @IBAction func case3(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio", withString: "case3")
    }
    
    @IBAction func aim_on(_ sender: UIButton) {mqttClient.publish("rpi/gpio", withString: "aim_on")
    }
    @IBAction func aim_off(_ sender: UIButton) {mqttClient.publish("rpi/gpio", withString: "aim_off")
    }
    @IBAction func runButton(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio", withString: "run")
    }
    @IBAction func right_horiz(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "horiz_180")
        }
    @IBAction func mid_horiz(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "horiz_90")
        }
    @IBAction func left_horiz(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "horiz_0")
        }
    @IBAction func up_vert(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "vert_180")
        }
    @IBAction func mid_vert(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "vert_90")
        }
    @IBAction func lower_vert(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "vert_0")
        }

    @IBAction func backButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "back")
        }
    @IBAction func spinrightButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "spinright")
        }
    @IBAction func spinleftButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "spinleft")
        }
    @IBAction func gripperclampButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "clamp")
        }
    @IBAction func gripperunclampedButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "unclamp")
        }
    @IBAction func STOPButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "stop")
        }
   
    @IBAction func servorelaxButton(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "ser_Relax")
        }
        
    @IBAction func gripperRelaxButton(_ sender: UIButton) {
             mqttClient.publish("rpi/gpio", withString: "grip_Relax")
        }
    @IBAction func run0p1(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "run_0.1")
        }
    @IBAction func run_0p3(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "run_0.3")
        }
        
    @IBAction func back_0p1(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "back_0.1")
        }
    @IBAction func back_0p3(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "back_0.3")
        }
    @IBAction func SR_0p1(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "SR_0.1")}
    @IBAction func SL_0p1(_ sender: UIButton) {
            mqttClient.publish("rpi/gpio", withString: "SL_0.1")}
    @IBAction func Flashlight_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "flashlight_on")}
    @IBAction func Flashlight_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "flashlight_off")
    }
    @IBAction func Laser_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "laser_on")
    }
    @IBAction func Laser_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "laser_off")
    }
    @IBAction func both_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "both_on")
    }
    @IBAction func both_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "both_off")
    }
    @IBAction func AI_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Follow_on")
    }
    @IBAction func AI_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Follow_off")
    }
    @IBAction func glove_on(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "glove_on")
    }
    @IBAction func Glove_off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "glove_off")
    }
    @IBAction func Fetch_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Fetch_On")
    }
    @IBAction func Fetch_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Fetch_Off")
    }
    @IBAction func Picture_1(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Picture_1")
        
    }
    @IBAction func Picture_On(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Picture_On")
    }
    @IBAction func Picture_Off(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "Picture_Off")
    }
    @IBAction func plus_twentyfive(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "plus_twentyfive")
        
    }
    @IBAction func plus_ten(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "plus_ten")
    }
    @IBAction func plus_five(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "plus_five")
    }
    @IBAction func plus_one(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "plus_one")
    }
    @IBAction func minus_twentyfive(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "minus_twentyfive")
    }
    @IBAction func minus_ten(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "minus_ten")
    }
    @IBAction func minus_five(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "minus_five")
    }
    @IBAction func minus_one(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "minus_one")
    }
    @IBAction func charge(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "charge")
    }
    @IBAction func step_to(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "step_to")
    }
    @IBAction func trigger(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "trigger")
    }
    @IBAction func reset(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "reset")
    }

    @IBAction func p_25(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "p_twentyfive")
    }
    @IBAction func p_ten(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "p_ten")
    }
    @IBAction func p_five(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "p_five")
    }
    @IBAction func p_one(_ sender: UIButton) {mqttClient.publish("rpi/gpio",withString: "p_one")
    }
    @IBAction func m_twentyfive(_ sender: UIButton) {mqttClient.publish("rpi/gpio",withString: "m_twentyfive")
    }
    @IBAction func m_ten(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "m_ten")
    }
    @IBAction func m_five(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "m_five")
    }
    @IBAction func m_one(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio",withString: "m_one")
    }
}

