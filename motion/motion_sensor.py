import RPi.GPIO as GPIO
import time
import threading
import paho.mqtt.publish as publish
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the PIR sensor
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# Variable to store motion detection status
motion_detected = False

def motion_sensor():
    global motion_detected
    print("Motion Sensor Initialized")
    print("Press Ctrl+C to exit")

    try:
        while True:
            if GPIO.input(PIR_PIN):
                motion_detected = True
                print("Motion Detected!")
                publish.single("g1g5.homeshield.levis.shopee", "motion", hostname="broker.hivemq.com") 
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
            print("Handling motion event...")
            motion_detected = False
            # You can add any additional processing here
            time.sleep(5)  # Optional delay to avoid handling too fast

except KeyboardInterrupt:
    print("Stopping the motion sensor thread...")

# Cleanup
motion_thread.join()  # Wait for the thread to finish
GPIO.cleanup()
