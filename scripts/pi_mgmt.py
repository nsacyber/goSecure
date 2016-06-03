import os
import RPi.GPIO as GPIO

def pi_reboot():
    os.system("sudo reboot")
    
def pi_shutdown():
    os.system("sudo shutdown -h now")
    
def start_ssh_service():
    os.system("sudo service ssh start")
    
def turn_on_led_green():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(7,GPIO.OUT)
    GPIO.output(7,GPIO.HIGH)
        
def turn_off_led_green():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(7,GPIO.OUT)
    GPIO.output(7,GPIO.LOW)