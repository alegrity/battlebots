#-------------------------------------------- Imports/General ----------------------------------------------------------------

import math
from Systems_Control import L298N_motorControl, MG995_servoControl

def moveXY(x, y):
    x = float(x)
    y = float(y)

    
    def get_motor_powers(x, y):
        x = max(-1, min(1, x))
        y = max(-1, min(1, y))

        # Initialize motor powers
        motor1_power = 0  # Left motor
        motor2_power = 0  # Right motor
        ax = abs(x)
        ay = abs(y)
        if x < 0:  # affects the right motor
            if ax < ay:
                motor1_power = ay - 0.5 * ax
                motor2_power = ay
            else:
                motor1_power = ay - 0.5 * ax
                motor2_power = ax
        else:  # affects the left motor
            if x < y:
                motor1_power = ay
                motor2_power = ay - 0.5 * ax
            else:
                motor1_power = ax
                motor2_power = ay - 0.5 * ax

        if y < 0:
            motor1_power = -motor1_power
            motor2_power = -motor2_power

        return motor1_power, motor2_power

    motor_left_power, motor_right_power = get_motor_powers(x, y)
    print(motor_left_power)
    print(motor_right_power)
    # Control the motors
    L298N_motorControl(float(motor_left_power), "Motor 1", 0)  # Left motor
    L298N_motorControl(float(motor_right_power), "Motor 2", 0)  # Right motor

def swingArm(x):
    MG995_servoControl(float(x), "Servo 1", 1, False)
