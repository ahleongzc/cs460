import RPi.GPIO as GPIO
import time
from light_sensor import read_light

LED_PIN = 18  # GPIO pin for the LED
LIGHT_THRESHOLD = 100  # Lux value below which we turn on the LED

def setup_led():
    """Set up the LED pin as an output."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

def set_led_on():
    """Turn the LED on."""
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED is ON")

def set_led_off():
    """Turn the LED off."""
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED is OFF")