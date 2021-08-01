import sys
import configparser

sys.path.append("../")
from pocca.utils.secrets import Secrets
from pocca.utils.system import System

settings = configparser.ConfigParser()
system = System()
secrets = Secrets()

settings.read("/media/usb/secrets.ini")
wifi_name = settings["WIFI"]["name"]
user_name = settings["USER"]["name"]
name = settings["USER"]["host"]

if(settings["ENCRYPT"]["enable"] == "true"):
  wifi_password = secrets.decode(settings["WIFI"]["password"])
  if wifi_password is False:
    print(".... Encrypt WiFi Password ....")
    wifi_password = settings["WIFI"]["password"]
    settings["WIFI"]["password"] = secrets.encode(settings["WIFI"]["password"])

  user_password = secrets.decode(settings["USER"]["password"])
  if user_password is False:
    print(".... Encrypt User Password ....")
    user_password = settings["USER"]["password"]
    settings["USER"]["password"] = secrets.encode(settings["USER"]["password"])

  with open("/media/usb/secrets.ini", "w") as configFile:
    settings.write(configFile)
else:
  wifi_password = settings["WIFI"]["password"]
  user_password = settings["USER"]["password"]

print("Setup wpa_supplicant.conf")
wpa_supplicant_file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
wpa_supplicant_file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
wpa_supplicant_file.write("update_config=1\n")
wpa_supplicant_file.write("country=" + settings["WIFI"]["country"]+"\n")
wpa_supplicant_file.write("network={\n")
wpa_supplicant_file.write("         ssid=\""+wifi_name+"\"\n")
wpa_supplicant_file.write("         psk=\""+wifi_password+"\"\n")
wpa_supplicant_file.write("}\n")
wpa_supplicant_file.close()


print(" Changing name to " + name)
system.change_name(name)

print(" Changing SSH password for " + user_name)
system.update_ssh_user(user_name, user_password)

print(" Changing SAMBA password for " + user_name)
system.update_samba_user(user_name, user_password)

print(" Connecting to " + wifi_name)
system.restart_wifi()
