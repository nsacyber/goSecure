import subprocess, urllib2

def get_wifi_list():
    iw_list = (subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"])).split("\n")

    #contains a tuple of the (ESSID, Encryption key)
    wifi_list = []

    for x in range(0, len(iw_list)):
        if((iw_list[x].strip())[0:5] == "ESSID"):
            if((iw_list[x].strip())[7:-1] != ""):
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
    
    process = subprocess.Popen(["sudo", "ifdown", "wlan0"])
    process.wait()
    process = subprocess.Popen(["sudo", "ifup", "wlan0"])
    process.wait()

def check_wifi_status():
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
