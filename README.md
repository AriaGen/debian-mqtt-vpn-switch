//Install what you'll need and set up a python vertual env. Adjust for your mqtt server.

sudo apt update
sudo apt install mosquitto-clients python3 python3-pip
sudo apt install python3.11-venv
python3 -m venv /opt/mqtt_listener_env
source /opt/mqtt_listener_env/bin/activate
pip install paho-mqtt

//create and install python script
mkdir /etc/vpnswitch
nano mqtt_service_listener.py

//create and install the service
sudo nano /etc/systemd/system/mqtt-listener.service

sudo systemctl daemon-reload
sudo systemctl enable mqtt-listener
sudo systemctl start mqtt-listener

//To check the status:
sudo systemctl status mqtt-listener

//Log output
sudo journalctl -u mqtt-listener -f


//Home assistant, create sensor:
mqtt:
  sensor:
    - name: "VPN-A IP Address"
      state_topic: "vpn/server-a/ip-addr"

//Publish to mqtt for control. Chance payload to on to switch on.
action: mqtt.publish
metadata: {}
data:
  topic: vpn/server-a/switch
  payload: "off"
