import RPi.GPIO as GPIO
import time
from message import send_message  # Import the send_message function

# Define the PIR sensor pin
PIR_PIN = 17

# Global variable to hold motion detection status
motion_detected_flag = False

def motion_detected(channel):
    """Handles the actions when motion is detected."""
    global motion_detected_flag
    print("Motion Detected!")
    send_message("Motion Detected!")  # Send message when motion is detected
    motion_detected_flag = True  # Set the flag when motion is detected

def setup_motion_sensor():
    """Sets up the PIR motion sensor and configures the event detection."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)  # Set PIR pin as input
    
    # Add event detection for rising edge (motion detected)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
    print("Motion Sensor Setup Complete. Waiting for motion...")

def cleanup_motion_sensor():
    """Cleans up the GPIO settings."""
    GPIO.remove_event_detect(PIR_PIN)  # Remove event detection
    GPIO.cleanup()
    print("GPIO cleaned up.")

def get_motion_status():
    """Returns the current motion detection status."""
    global motion_detected_flag
    return motion_detected_flag

def reset_motion_status():
    """Resets the motion detection status flag."""
    global motion_detected_flag
    motion_detected_flag = False
