#-------------------------------------------- Imports/General ----------------------------------------------------------------

import network
import time
import machine


WIFI_SSID = 'PicoW_AP'
WIFI_PASSWORD = '12345678'



ONBOARD_LED = machine.Pin("LED", machine.Pin.OUT)
ONBOARD_LED.off()
led2 = machine.Pin(14, machine.Pin.OUT) 

MOTOR_PINS = {
    "Motor 1" : [4,3,2],
    "Motor 2" : [],
    "Servo 1" : [5],
    "DC 1": [],
}


def joystick(joy_x, joy_y):
    print(f'joy-x: {joy_x}; joy-y: {joy_y}')

def slider(slider_value):
    print(f'slider: {slider_value}')
        
def turn_on_led1():
    # print("Turning on")
    ONBOARD_LED.on()

def turn_off_led1():
    ONBOARD_LED.off()

def turn_on_led2():
    led2.on()

def turn_off_led2():
    led2.off()


#-------------------------------------------- AP Setup -----------------------------------------------------------------

def setup_wifi_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    ap.config(ssid=WIFI_SSID, password=WIFI_PASSWORD)
    ap.active(True)
    while not ap.active():
        # print("Activation Failed")
        pass
    print('Access point active:', ap.ifconfig())
    turn_on_led1()
    time.sleep(1)
    turn_off_led1()

def run_setup():
    turn_on_led1()
    time.sleep(1)
    turn_off_led1()
    setup_wifi_ap()
