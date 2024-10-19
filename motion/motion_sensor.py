import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the PIR sensor
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

print("Motion Sensor Initialized")
print("Press Ctrl+C to exit")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
            time.sleep(1)  # Delay to avoid multiple triggers
        else:
            print("No Motion")
            time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
