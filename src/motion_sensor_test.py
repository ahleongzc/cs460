import RPi.GPIO as GPIO
import time
import threading
import paho.mqtt.publish as publish

from motion_sensor import setup_motion_sensor, cleanup_motion_sensor, get_motion_status, reset_motion_status
from light_sensor import read_light
from led_control import set_led_off, set_led_on, setup_led
import time

# Setup the sensors and devices
setup_led()
LIGHT_THRESHOLD = 100  # Set your light threshold (in Lux)

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the PIR sensor
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# Variable to store motion detection status
motion_detected = False

import paho.mqtt.client as mqtt
import threading
import time
import datetime

mqttc = None
counter = 0

def start_publisher_thread():
    global mqttc
    broker = "broker.hivemq.com"
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    def on_publish(client, userdata, mid, reason_code, properties): 
        print("published")
        
    mqttc.on_publish = on_publish
    mqttc.connect(broker, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    
    thread = threading.Thread(target=mqttc.loop_forever)
    thread.start()

start_publisher_thread()

def motion_sensor():
    global motion_detected
    print("Motion Sensor Initialized")
    print("Press Ctrl+C to exit")

    try:
        while True:
            if GPIO.input(PIR_PIN):
                motion_detected = True
                print("Motion Detected!")
                time.sleep(1)  # Delay to avoid multiple triggers
            else:
                motion_detected = False
                time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        GPIO.cleanup()

# Create and start the motion sensor thread
motion_thread = threading.Thread(target=motion_sensor)
motion_thread.start()

# Main program loop
try:
    while True:
        if motion_detected:
            print("Motion Detected!")
            counter += 1
            print(f"the counter is {counter} at {datetime.datetime.now()}")
            if counter == 300:
                mqttc.publish("g1g5.homeshield.levis.shopee", "motion", qos=1)
                print("Reset") 
                counter = 0
                
                # Handle motion detected event
                print("Handling motion event...")

                light_intensity = read_light()  # Read the light level

                if light_intensity is not None:
                    print(f"Current Light Intensity: {light_intensity:.2f} Lux")

                    if light_intensity < LIGHT_THRESHOLD:  # If light intensity is below threshold
                        print("Light is dim, turning on the LED.")
                        set_led_on()  # Turn on the LED
                    else:
                        print("Light is sufficient, LED stays off.")
                        set_led_off()  # Ensure the LED is off if light is sufficient

                time.sleep(5)  # Keep the LED on for 10 seconds if light is dim
                set_led_off()

                motion_detected = False
                
                for i in range(20):
                    print(f"the time left for next motion to be detected is {i}")
                    time.sleep(i)
                # You can add any additional processing here
                # time.sleep(2)  # Optional delay to avoid handling too fast

except KeyboardInterrupt:
    print("Stopping the motion sensor thread...")

# Cleanup
motion_thread.join()  # Wait for the thread to finish
GPIO.cleanup()
