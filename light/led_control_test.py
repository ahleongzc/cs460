import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number for the LED
LED_PIN = 18  # Change this if you're using a different GPIO pin

# Set up the LED pin as an output
GPIO.setup(LED_PIN, GPIO.OUT)

# Start the while loop for continuous input
while True:
    # Ask the user for input
    user_input = input("Enter 'on' to turn the LED on, 'off' to turn the LED off, or 'exit' to quit: ").strip().lower()

    # Check user input and control the LED accordingly
    if user_input == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED is ON")
    elif user_input == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED is OFF")
    elif user_input == 'exit':
        print("Exiting program...")
        break  # Exit the while loop if the user enters 'exit'
    else:
        print("Invalid input. Please enter 'on', 'off', or 'exit'.")

# Clean up GPIO settings when the loop ends
GPIO.cleanup()
