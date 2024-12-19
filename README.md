//Install what you'll need and set up a python vertual env. Adjust for your mqtt server.<br>

sudo apt update<br>
sudo apt install mosquitto-clients python3 python3-pip<br>
sudo apt install python3.11-venv<br>
python3 -m venv /opt/mqtt_listener_env<br>
source /opt/mqtt_listener_env/bin/activate<br>
pip install paho-mqtt<br>
<br>
//create and install python script<br>
mkdir /etc/vpnswitch<br>
cd /etc/vpnswitch<br>
nano mqtt_service_listener.py<br>
<br>
//create and install the service<br>
sudo nano /etc/systemd/system/mqtt-listener.service<br>
<br>
sudo systemctl daemon-reload<br>
sudo systemctl enable mqtt-listener<br>
sudo systemctl start mqtt-listener<br>
<br>
//To check the status:<br>
sudo systemctl status mqtt-listener<br>
<br>
//Log output<br>
sudo journalctl -u mqtt-listener -f<br>
<br>
//Home assistant, create sensor:<br>
mqtt:<br>
  sensor:<br>
    - name: "VPN-A IP Address"<br>
      state_topic: "vpn/server-a/ip-addr"<br>
<br>
//Publish to mqtt for control. Chance payload to on to switch on.<br>
action: mqtt.publish<br>
metadata: {}<br>
data:<br>
  topic: vpn/server-a/switch<br>
  payload: "off"<br>
