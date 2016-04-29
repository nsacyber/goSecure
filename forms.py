from wtforms import PasswordField, SelectField, SubmitField, StringField, validators 
from flask.ext.wtf import Form
from scripts.rpi_wifi_conn import get_wifi_list

class initialSetupForm(Form):
    wifi_list = get_wifi_list()
    ssid = SelectField("Network Name", choices=wifi_list)
    #ssid = SelectField("Network Name", choices=[("Wifi 1","Wifi 1"),("Wifi 2", "Wifi 2")])
    psk = PasswordField("Password", [validators.DataRequired()])

    vpn_server = StringField("Server Hostname", [validators.DataRequired("Please enter the goSecure Server Hostname or IP Address."), validators.Length(max=255, message="Please enter a goSecure Server Hostname or IP Address between 0 and 255 characters.")])
    user_id = StringField("VPN User ID", [validators.DataRequired("Please enter the goSecure User Id."), validators.Length(max=255, message="Please enter a goSecure User Id between 0 and 255 characters.")])
    user_psk = PasswordField("VPN PSK", [validators.DataRequired()]) 
    initialSetupSubmit = SubmitField("Save", [validators.DataRequired()])