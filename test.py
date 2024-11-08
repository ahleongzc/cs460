import paho.mqtt.client as mqtt
import threading
import time

mqttc = None

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

import RPi.GPIO as GPIO
import time
import threading
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the PIR sensor
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# Variable to store motion detection status
motion_detected = False
counter = 0

def motion_sensor():
    global motion_detected
    print("Motion Sensor Initialized")
    print("Press Ctrl+C to exit")

    try:
        while True:
            if GPIO.input(PIR_PIN):
                motion_detected = True
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
            # Handle motion detected event
            print("Motion Detected!")
            motion_detected = False
            counter += 1
            if counter == 10:
                mqttc.publish("g1g5.homeshield.levis.shopee", "motion", qos=1)
                counter = 0
            # You can add any additional processing here
            time.sleep(5)  # Optional delay to avoid handling too fast

except KeyboardInterrupt:
    print("Stopping the motion sensor thread...")

# Cleanup
motion_thread.join()  # Wait for the thread to finish
GPIO.cleanup()
