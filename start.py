#-------------------------------------------- Imports/General ----------------------------------------------------------------

import network
import time
import machine


WIFI_SSID = 'PicoW_AP'
WIFI_PASSWORD = '12345678'



ONBOARD_LED = machine.Pin("LED", machine.Pin.OUT)
ONBOARD_LED.off()
spinner = machine.Pin(0, machine.Pin.OUT)

MOTOR_PINS = {
    "Motor 1" : [2,3,8],
    "Motor 2" : [4,5,7],
    "Servo 1" : [6],
    "DC 1": [],
}


def joystick(joy_x, joy_y):
    print(f'joy-x: {joy_x}; joy-y: {joy_y}')

def slider(slider_value):
    print(f'slider: {slider_value}')
        
def button_1():
    # print("Turning on")
    spinner.on()

def button_2():
    spinner.off()

def button_3():
    ONBOARD_LED.on()

def button_4():
    ONBOARD_LED.off()


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
    ONBOARD_LED.on()
    time.sleep(1)
    ONBOARD_LED.off()

def run_setup():
    ONBOARD_LED.on()
    time.sleep(1)
    ONBOARD_LED.off()
    setup_wifi_ap()
