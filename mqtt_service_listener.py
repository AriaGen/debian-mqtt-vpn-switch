#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import subprocess
import sys
import threading
import time

# Configuration
MQTT_BROKER = "192.168.1.0"         # MQTT broker address
MQTT_PORT = 1883                    # Default MQTT port
MQTT_TOPIC = "vpn/server-a/switch"  # Topic for VPN control
IP_TOPIC = "vpn/server-a/ip-addr"   # Topic for publishing IP address
USERNAME = "mqtt"                   # MQTT username
PASSWORD = "****"            # MQTT password
SERVICE_NAME = "openvpn"            # Service to start/stop
IP_CHECK_INTERVAL = 60              # Interval (in seconds) for checking the IP address

# Function to start a service
def start_service():
    print("Starting the service...")
    subprocess.run(["systemctl", "start", SERVICE_NAME])

# Function to stop a service
def stop_service():
    print("Stopping the service...")
    subprocess.run(["systemctl", "stop", SERVICE_NAME])

# Function to fetch and publish the public IP address
def publish_ip_address():
    while True:
        try:
            # Fetch the public IP address
            result = subprocess.run(["curl", "-s", "ifconfig.me"], capture_output=True, text=True)
            ip_address = result.stdout.strip()
            if ip_address:
                print(f"Fetched IP Address: {ip_address}")
                client.publish(IP_TOPIC, ip_address)  # Publish the IP address to MQTT
                print(f"Published IP Address to {IP_TOPIC}")
        except Exception as e:
            print(f"Error fetching or publishing IP address: {e}")
        time.sleep(IP_CHECK_INTERVAL)  # Wait for the configured interval

# The callback when the client receives a message from the broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8").strip().lower()
    print(f"Received message: {payload}")
    
    if payload == "on":
        start_service()
    elif payload == "off":
        stop_service()
    else:
        print(f"Unknown command: {payload}")

# The callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

# MQTT Client setup
client = mqtt.Client()

# Set username and password for MQTT
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
try:
    print("Connecting to broker...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the IP address publishing thread
    threading.Thread(target=publish_ip_address, daemon=True).start()

    # Start MQTT loop
    client.loop_forever()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
