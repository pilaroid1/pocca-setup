import sys
sys.path.append("/media/usb/apps")
from pocca.utils.app import App

app = App()
app.clear_terminal()

wifi_name = app.secrets["WIFI"]["name"]
user_name = app.secrets["USER"]["name"]
name = app.settings["APPLICATION"]["name"]

if(app.settings["APPLICATION"]["encrypt"] == "1"):
  wifi_password = app.decoder.decode(app.secrets["WIFI"]["password"])
  if wifi_password is False:
    print(".... Encrypt WiFi Password ....")
    wifi_password = app.secrets["WIFI"]["password"]
    app.secrets["WIFI"]["password"] = app.decoder.encode(app.secrets["WIFI"]["password"])

  user_password = app.decoder.decode(app.secrets["USER"]["password"])
  if user_password is False:
    print(".... Encrypt User Password ....")
    user_password = app.secrets["USER"]["password"]
    app.secrets["USER"]["password"] = app.decoder.encode(app.secrets["USER"]["password"])

  with open("/media/usb/secrets.ini", "w") as configFile:
    app.secrets.write(configFile)
else:
  wifi_password = app.secrets["WIFI"]["password"]
  user_password = app.secrets["USER"]["password"]

print("Setup wpa_supplicant.conf")
wpa_supplicant_file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
wpa_supplicant_file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
wpa_supplicant_file.write("update_config=1\n")
wpa_supplicant_file.write("country=" + app.secrets["WIFI"]["country"]+"\n")
wpa_supplicant_file.write("network={\n")
wpa_supplicant_file.write("         ssid=\""+wifi_name+"\"\n")
wpa_supplicant_file.write("         psk=\""+wifi_password+"\"\n")
wpa_supplicant_file.write("}\n")
wpa_supplicant_file.close()

print(" Changing name to " + name)
app.system.change_name(name)

print(" Changing SSH password for " + user_name)
print(user_password)
app.system.change_ssh_user(user_name, user_password)

print(" Changing SAMBA password for " + user_name)
app.system.change_samba_user(user_name, user_password)

if app.settings["APPLICATION"]["type"] != app.system.info["current_app"]:
  print("Changing application from " + app.system.info["current_app"] + " to " + app.settings["APPLICATION"]["type"])
  app.system.change_app(app.settings["APPLICATION"]["type"])

print(" Connecting to " + wifi_name)
app.system.change_wifi()
