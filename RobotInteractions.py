#-------------------------------------------- Imports ----------------------------------------------------------------

from Systems_Control import L298N_motorControl, MG995_servoControl
from start import MOTOR_PINS


#-------------------------------------------- Robot Stuff (Edit Stuff Here!) -----------------------------------------------------------------

def moveXY(x, y):
    L298N_motorControl(float(y),"Motor 1", 10)
    # motor2 = motorControl(y,"Motor_2", 10)
    MG995_servoControl(float(x), "Servo 1", 1, True)

def swingArm(x):
    MG995_servoControl(float(x), "Servo 1", 1, False)

