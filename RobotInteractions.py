#-------------------------------------------- Imports/General ----------------------------------------------------------------

from start import math
from Systems_Control import L298N_motorControl, MG995_servoControl, joystickToDiff

def moveXY(x, y):
    x = float(x)
    y = float(y)
    motor_left_power, motor_right_power = joystickToDiff(x, y,-1,1,-1,1)
    print(motor_left_power)
    print(motor_right_power)
    # Control the motors
    L298N_motorControl(float(motor_left_power), "Motor 1", 0)  # Left motor
    L298N_motorControl(float(motor_right_power), "Motor 2", 0)  # Right motor

def swingArm(x):
    MG995_servoControl(float(x), "Servo 1", 1, False)
