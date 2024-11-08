from motion_sensor import setup_motion_sensor, cleanup_motion_sensor, get_motion_status, reset_motion_status
from light_sensor import read_light
from led_control import set_led_off, set_led_on, setup_led
import time

# Setup the sensors and devices
setup_motion_sensor()
setup_led()

LIGHT_THRESHOLD = 100  # Set your light threshold (in Lux)

try:
    while True:
        if get_motion_status():  # If motion is detected
            print("Motion detected, performing action...")

            light_intensity = read_light()  # Read the light level

            if light_intensity is not None:
                print(f"Current Light Intensity: {light_intensity:.2f} Lux")

                if light_intensity < LIGHT_THRESHOLD:  # If light intensity is below threshold
                    print("Light is dim, turning on the LED.")
                    set_led_on()  # Turn on the LED
                else:
                    print("Light is sufficient, LED stays off.")
                    set_led_off()  # Ensure the LED is off if light is sufficient

                time.sleep(10)  # Keep the LED on for 10 seconds if light is dim

            reset_motion_status()  # Reset the motion detection flag
            time.sleep(2)  # Optional delay to avoid rapid detection of the same motion event
        else:
            print("Waiting for motion...")
            time.sleep(1)  # No motion, continue to wait

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    cleanup_motion_sensor()  # Clean up GPIO when exiting the program
