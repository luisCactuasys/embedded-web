#!/usr/bin/env python3
import os
import urllib.parse as urlparse
import datetime
import RPi.GPIO as GPIO
import threading
import time
import requests  # Import the requests library for HTTP communication


# Get the directory of the script and build relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(BASE_DIR, 'settings.log')
cert_file = os.path.join(BASE_DIR, 'cert.pem')

NOTIFY_SERVER_URL = "https://192.168.1.104:5000/notify"  # Replace with the actual server URL


# Function to log events
def log_event(setting):
    with open(log_file, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - Setting changed to: {setting}\n")

# Function to handle PWM in the background
def pwm_control(duty_cycle):
    try:
        with open(f"/sys/class/pwm/pwmchip0/pwm0/duty_cycle", "a") as f:
            f.write(str(duty_cycle))
    except IOError as e:
            log_event(f"Error setting up GPIO value: {e}")

# Function to notify another server of the updated duty cycle
def notify_other_server(duty_cycle):
    try:
        response = requests.post(NOTIFY_SERVER_URL, json={"duty_cycle": duty_cycle}, verify=cert_file)
        if response.status_code == 200:
            log_event(f"Successfully notified server with duty cycle: {duty_cycle}")
            print(f"Successfully notified server with duty cycle: {duty_cycle}")
        else:
            log_event(f"Error setting up GPIO value: {e}")
            print(f"Failed to notify server. Status code: {response.status_code}")
    except Exception as e:
        log_event(f"Error notifying server: {str(e)}")
        print(f"Error notifying server: {str(e)}")


# Get the query string from the environment
query_string = os.environ.get('QUERY_STRING', '')

# Parse the query string
query_params = urlparse.parse_qs(query_string)
brightness = query_params.get('brightness', [''])[0]  # Default to empty string if not provided

# Handle the brightness setting
if brightness.isdigit():
    duty_cycle = int(brightness)
    if 0 <= duty_cycle <= 100:
        pwm_control(duty_cycle*10000)

        # Notify the other server about the duty cycle update
        notify_other_server(duty_cycle)

        status = f"LED brightness set to {duty_cycle}%"
        log_event(f"Brightness set to {duty_cycle}%")
    else:
        status = "Invalid brightness value. Must be between 0 and 100."
else:
    status = "Unknown command"

# Output the response (HTML format)
print("Content-Type: text/html\n")
print(f"<html><body><h1>{status}</h1></body></html>")
