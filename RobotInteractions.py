#-------------------------------------------- Imports ----------------------------------------------------------------

from Systems_Control import L298N_motorControl, MG995_servoControl
from start import MOTOR_PINS


#-------------------------------------------- Robot Stuff (Edit Stuff Here!) -----------------------------------------------------------------

def moveXY(x, y):
    L298N_motorControl(float(y),"Motor 1", 0)
    # motor2 = motorControl(y,"Motor_2", 10)
    MG995_servoControl(float(y), "Servo 1", 0)

