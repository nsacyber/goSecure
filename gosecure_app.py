#!/usr/bin/env python

from flask import Flask, render_template, request, flash
from forms import initialSetupForm
from scripts.rpi_wifi_conn import add_wifi, check_wifi_status, reset_wifi
from scripts.vpn_server_conn import set_vpn_params, reset_vpn_params, start_vpn, stop_vpn, restart_vpn
from scripts.pi_mgmt import pi_reboot, pi_shutdown
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def initial_setup():
    form = initialSetupForm()

    if(request.method == "GET"):
        return render_template("index.html", form=form) 

    if(request.method == "POST"):
        if(form.validate()):
            ssid = (form.ssid.data).rsplit("-", 1)[0]
            psk = form.psk.data
            add_wifi(ssid, psk)
            
            time.sleep(15)
            
            if(check_wifi_status() == True):
                vpn_server = form.vpn_server.data
                user_id = form.user_id.data
                user_psk = form.user_psk.data
                set_vpn_params(vpn_server, user_id, user_psk)
            
                flash("Wifi and VPN settings saved!", "success")
                return render_template("index.html", form=form)
            else:
                flash("Error! Cannot reach the internet...", "error")
                return render_template("index.html", form=form)
            
        else:
            flash("Error! " + str(form.data), "error")
            return render_template("index.html", form=form)

    else:
        return render_template("index.html", form=form)

@app.route("/action", methods=["POST"])
def execute_action():
    action = request.form["action"]
    if(action == "reboot"):
        pi_reboot()
    elif(action == "shutdown"):
        pi_shutdown()
    elif(action == "reset_settings"):
        form = initialSetupForm()
        reset_wifi()
        reset_vpn_params()
        flash("Wifi and VPN settings reset!", "notice")
        return render_template("index.html", form=form)
    elif(action == "start_vpn"):
        form = initialSetupForm()
        start_vpn()
        flash("VPN Started!", "notice")
        return render_template("index.html", form=form)
    elif(action == "stop_vpn"):
        form = initialSetupForm()
        stop_vpn()
        flash("VPN Stopped!", "notice")
        return render_template("index.html", form=form)
    elif(action == "restart_vpn"):
        form = initialSetupForm()
        restart_vpn()
        flash("VPN Restarted!", "notice")
        return render_template("index.html", form=form)
    else:
        form = initialSetupForm()
        flash("Error! Invalid Action!", "error")
        return render_template("index.html", form=form)

if __name__ == "__main__":
    app.secret_key="goSecureSecretKeyForCSRF"
    #app.run(host="192.168.50.1", port=80, debug=True)
    app.run(host="192.168.50.1", port=80)
