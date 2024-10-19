import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number for the LED
LED_PIN = 18  # Change this if you're using a different GPIO pin

# Set up the LED pin as an output
GPIO.setup(LED_PIN, GPIO.OUT)

# Turn on the LED
GPIO.output(LED_PIN, GPIO.HIGH)
print("LED is ON")

# Keep the LED on for 5 seconds
time.sleep(5)

# Turn off the LED
GPIO.output(LED_PIN, GPIO.LOW)
print("LED is OFF")

# Clean up GPIO settings
GPIO.cleanup()
