import os

def pi_reboot():
    os.system("sudo reboot")
    
def pi_shutdown():
    os.system("sudo shutdown -h now")