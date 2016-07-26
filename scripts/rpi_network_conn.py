from subprocess import CalledProcessError, check_output, Popen
import wifi_captive_portal
import urllib2
import time

def get_wifi_list():
    try:
        wlan_status = check_output(["sudo", "ifup", "wlan0"])
        returncode = 0
    except CalledProcessError as e:
        returncode = e.returncode

    try:
        iw_list = (check_output(["sudo", "iwlist", "wlan0", "scan"])).split("\n")
    except CalledProcessError as e:
        iw_list = []

    #contains a tuple of the (ESSID, Encryption key)
    wifi_list = []

    for x in range(0, len(iw_list)):
        if((iw_list[x].strip())[0:5] == "ESSID"):
            if((iw_list[x].strip())[7:-1] != "" and (not ( iw_list[x].strip())[7:-1].startswith("\\"))):
                wifi_list.append((((iw_list[x].strip())[7:-1] + "-" + ((iw_list[x-1].strip())[15:])), (iw_list[x].strip())[7:-1]))

    return sorted(list(set(wifi_list)), key=lambda wifilist: wifilist[0])

def add_wifi(wifi_ssid, wifi_key):
    with open("/etc/wpa_supplicant/wpa_supplicant.conf") as wpa_supplicant:
        lines = wpa_supplicant.readlines()
    
    wifi_exists = False
    for x in range(0, len(lines)):
        #if SSID is already in file
        if((lines[x].strip()) == 'ssid="' + str(wifi_ssid) + '"'):
            wifi_exists = True
            lines[x] = '    ssid="%s"\n' % (wifi_ssid)
            if(wifi_key == "key_mgmt_none"):
                lines[x+1] = '    key_mgmt=NONE\n'
            else:
                lines[x+1] = '    psk="%s"\n' % (wifi_key)
                
    if(wifi_exists != True):
        lines.append('network={\n')
        lines.append('    ssid="%s"\n' % (wifi_ssid))
        if(wifi_key == "key_mgmt_none"):
            lines.append('    key_mgmt=NONE\n')
        else:
            lines.append('    psk="%s"\n' % (wifi_key))  
        lines.append('}\n')

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as fout:
        for line in lines:
            fout.write(line)
    
    process = Popen(["sudo", "ifdown", "wlan0"])
    process.wait()
    process = Popen(["sudo", "ifup", "wlan0"])
    process.wait()
    
    time.sleep(15)
    
    if(not internet_status()):
        wifi_captive_portal.captive_portal(wifi_ssid, "", "")

def internet_status():
    try:
        response = urllib2.urlopen("https://aws.amazon.com",timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def reset_wifi():
    lines = []
    lines.append("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    lines.append("update_config=1\n")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as fout:
        for line in lines:
            fout.write(line)
    
    try:
        vpn_status = (check_output(["sudo", "ifdown", "wlan0"]))
        returncode = 0
    except CalledProcessError as e:
        returncode = e.returncode

    if(returncode == 0):
        return True
    else:
        return False