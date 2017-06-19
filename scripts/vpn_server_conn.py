from subprocess import CalledProcessError, check_output
import time
from pi_mgmt import turn_on_led_green, turn_off_led_green


def set_vpn_params(vpn_server, user_id, user_psk):
    # set the goSecure server IP address in the ipsec.conf file
    with open("/etc/ipsec.conf") as fin:
        lines = fin.readlines()

    for x in range(0, len(lines)):
        if((lines[x].strip())[0:7] == "leftid="):
            lines[x] = "        leftid=%s       #unique id of client\n" % user_id
        if((lines[x].strip())[0:6] == "right="):
            lines[x] = "        right=%s       #strongSwan server external IP\n" % vpn_server

    with open("/etc/ipsec.conf", "w") as fout:
        for line in lines:
            fout.write(line)

    # save the username and secret to the ipsec.secrets file
    secrets = open("/etc/ipsec.secrets", "w")
    secrets.write("%s : PSK %s" % (user_id, user_psk))
    secrets.close()


def reset_vpn_params():
    set_vpn_params("<eth0_ip_of_server>", "<unique_id_of_client>", "<password_for_client>")
    stop_vpn()


# add route for accessing local ip addresses on the LAN interface (prevents getting locked out from the goSecure Client web gui)
def add_route():
    route_table_list = check_output(["ip", "route", "show", "table", "220"]).split("\n")
    
    if "192.168.50.0/24 dev eth0  scope link" not in route_table_list:
        try:
            check_output(["sudo", "ip", "route", "add", "table", "220", "192.168.50.0/24", "dev", "eth0"])
            returncode = 0
        except CalledProcessError as e:
                returncode = e.returncode
                
        if(returncode == 0):
                return True
        else:
            return False
        
    else:
        return True


def start_vpn():
    try:
        check_output(["sudo", "ipsec", "start"])
        returncode = 0
        time.sleep(10)
    except CalledProcessError as e:
        returncode = e.returncode
        
    if(returncode == 0):
        if(vpn_status()):
            if(add_route):
                time.sleep(3)
                turn_on_led_green()
                return True

    else:
        return False


def stop_vpn():
    try:
        check_output(["sudo", "ipsec", "stop"])
        returncode = 0
        turn_off_led_green()
    except CalledProcessError as e:
        returncode = e.returncode
    
    if(returncode == 0):
        return True
    else:
        return False


def restart_vpn():
    turn_off_led_green()
    
    try:
        check_output(["sudo", "ipsec", "restart"])
        returncode = 0
        time.sleep(10)
    except CalledProcessError as e:
        returncode = e.returncode
    
    if(returncode == 0):
        if(vpn_status()):
            if(add_route()):
                time.sleep(3)
                turn_on_led_green()
                return True
    else:
        return False


def vpn_status():
    try:
        vpn_status = (check_output(["sudo", "ipsec", "status"])).split("\n")
        returncode = 0
    except CalledProcessError as e:
        returncode = e.returncode
    
    # if ipsec status command ran successfully, check if tunnel is established
    if(returncode == 0):
        if((vpn_status[1].strip())[9:20] == "ESTABLISHED"):
            return True

    return False


def vpn_configuration_status():
    leftid_set = 0  # unique id of client
    right_set = 0  # strongSwan server external IP or DNS name
    vpn_psk = 0  # unique id of client and psk for VPN

    # check to see if the leftid, and right are set in the ipsec.conf file
    with open("/etc/ipsec.conf") as fin:
        lines = fin.readlines()

    for x in range(0, len(lines)):
        if((lines[x].strip())[0:7] == "leftid="):
            if((lines[x].strip())[7:28] != "<unique_id_of_client>"):
                leftid_set = 1
        if((lines[x].strip())[0:6] == "right="):
            if((lines[x].strip())[6:25] != "<eth0_ip_of_server>"):
                right_set = 1

    # check to see if the username and secret are set in the ipsec.secrets file
    with open("/etc/ipsec.secrets") as fin:
        lines = fin.readlines()

        if((lines[0].strip())[0:49] != "<unique_id_of_client> : PSK <password_for_client>"):
            vpn_psk = 1

    if(leftid_set == 1 and right_set == 1 and vpn_psk == 1):
        return True
    else:
        return False
