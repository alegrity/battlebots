#-------------------------------------------- Imports ----------------------------------------------------------------

from start import machine as m, MOTOR_PINS, time, math

#-------------------------------------------- Motor Control -----------------------------------------------------------------



def L298N_motorControl(speedval, motor: str, duration):
    pins = MOTOR_PINS[motor]
    IN1 = m.Pin(pins[0], m.Pin.OUT)
    IN2 = m.Pin(pins[1], m.Pin.OUT)
    
    # Create PWM object for speed control
    speed_pwm = m.PWM(m.Pin(pins[2], m.Pin.OUT))
    speed_pwm.freq(1000)
    
    if speedval > 0:
        direction = "Forward"
    elif speedval < 0:
        direction = "Backward"
    else:
        direction = "Stop"
    
    # Convert speed value
    speedval = convertSpeed(speedval)
    
    # Debugging
    print(f"Motor: {motor}, Direction: {direction}, Speed Value: {speedval}")
    
    if direction != "Stop":
        # Set PWM duty cycle
        speed_pwm.duty_u16(speedval)
    
    if direction == "Forward":
        IN1.low()
        IN2.high()
    elif direction == "Backward":
        IN1.high()
        IN2.low()
    elif direction == "Stop":
        IN1.low()
        IN2.low()
        # Stop PWM output
        speed_pwm.duty_u16(0)
    
    time.sleep_ms(duration)

def convertSpeed(speed):
    speed = int(abs(speed) * 45535)
   
    if speed <= 65535:
        return speed
    else:
        return 65535
    
# def get_motor_powers(x, y):
#     angle = math.atan2(x,y)
#     left_mod = 
#     right_mod = 
#     left_power = y*left_mod
#     right_power = y*right_mod

    # x = max(-1, min(1, x))
    # y = max(-1, min(1, y))

    # # Initialize motor powers
    # motor1_power = 0  # Left motor
    # motor2_power = 0  # Right motor
    # ax = abs(x)
    # ay = abs(y)
    # if x < 0:  # affects the right motor
    #     if ax < ay:
    #         motor1_power = ay - 0.5 * ax
    #         motor2_power = ay
    #     else:
    #         motor1_power = ay - 0.5 * ax
    #         motor2_power = ax
    # else:  # affects the left motor
    #     if x < y:
    #         motor1_power = ay
    #         motor2_power = ay - 0.5 * ax
    #     else:
    #         motor1_power = ax
    #         motor2_power = ay - 0.5 * ax

    # if y < 0:
    #     motor1_power = -motor1_power
    #     motor2_power = -motor2_power

    # return motor1_power, motor2_power

def joystickToDiff(x, y, minJoystick, maxJoystick, minSpeed, maxSpeed):	# If x and y are 0, then there is not much to calculate...
	if x == 0 and y == 0:
		return (0, 0)
    

	# First Compute the angle in deg
	# First hypotenuse
	z = math.sqrt(x * x + y * y)

	# angle in radians
	rad = math.acos(math.fabs(x) / z)

	# and in degrees
	angle = rad * 180 / math.pi

	# Now angle indicates the measure of turn
	# Along a straight line, with an angle o, the turn co-efficient is same
	# this applies for angles between 0-90, with angle 0 the coeff is -1
	# with angle 45, the co-efficient is 0 and with angle 90, it is 1

	tcoeff = -1 + (angle / 90) * 2
	turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
	turn = round(turn * 100, 0) / 100

	# And max of y or x is the movement
	mov = max(math.fabs(y), math.fabs(x))

	# First and third quadrant
	if (x >= 0 and y >= 0) or (x < 0 and y < 0):
		rawLeft = mov
		rawRight = turn
	else:
		rawRight = mov
		rawLeft = turn

	# Reverse polarity
	if y < 0:
		rawLeft = 0 - rawLeft
		rawRight = 0 - rawRight

	# minJoystick, maxJoystick, minSpeed, maxSpeed
	# Map the values onto the defined rang
	rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
	leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

	return (rightOut, leftOut)
def map(v, in_min, in_max, out_min, out_max):
	# Check that the value is at least in_min
	if v < in_min:
		v = in_min
	# Check that the value is at most in_max
	if v > in_max:
		v = in_max
	return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def MG995_servoControl(angleval, motor: str, wait, Center:bool):
    pins = MOTOR_PINS[motor]
    if Center: angleval = convertDutyCentered(angleval, 4680, 3276)
    else: angleval = convertDuty(angleval, 1639, 8191)
    print(angleval)
    angle = m.PWM(m.Pin(pins[0]))
    angle.freq(50)
    angle.duty_u16(angleval)
    time.sleep_ms(wait)

def convertDutyCentered(angle, center, offset):
    return int(abs((offset*angle)+center))

def convertDuty(angle, zero, maximum):
    return int(abs(((angle/100)*(maximum-zero))+zero))
