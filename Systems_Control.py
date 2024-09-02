#-------------------------------------------- Imports ----------------------------------------------------------------

from start import machine as m, MOTOR_PINS, time

#-------------------------------------------- Motor Control -----------------------------------------------------------------

def L298N_motorControl(speedval, motor: str, duration):
    pins = MOTOR_PINS[motor]
    IN1 = m.Pin(pins[1], m.Pin.OUT)
    IN2 = m.Pin(pins[2], m.Pin.OUT)
    if speedval > 0: direction = "Forward"
    elif speedval < 0: direction = "Backward"
    else: direction = "Stop"
    if direction != "Stop":
        speedval = convertSpeed(speedval)
        speed = m.PWM(m.Pin(pins[0], m.Pin.OUT))
        speed.freq(1000)
        speed.duty_u16(speedval)
    if direction == "Forward":
        IN1.low()
        IN2.high()
    elif direction == "Backward":
        IN1.high()
        IN2.low()
    elif direction == "Stop":
        IN1.low()
        IN2.low()
    time.sleep_ms(duration)

def convertSpeed(speed):
    speed = int(abs(speed*65535))
    if speed <= 65535: return speed 
    elif speed > 65535: return 65535

def MG995_servoControl(angleval, motor: str, wait):
    pins = MOTOR_PINS[motor]
    angleval = convertDuty(angleval)
    print(angleval)
    angle = m.PWM(m.Pin(pins[0]))
    angle.freq(50)
    angle.duty_u16(angleval)
    time.sleep_ms(wait)
    angle.deinit()

def convertDuty(angle):
    return int((3031*angle)+4833)
