
import RPi.GPIO as GPIO
import smbus
import time

# GPIO pin configuration
ADO_PIN = 23  # ADO pin for the light sensor
SDA_PIN = 24  # SDA pin for I²C
SCL_PIN = 25  # SCL pin for I²C

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ADO_PIN, GPIO.IN)  # Set ADO pin as input

# Create I²C bus
bus = smbus.SMBus(1)

# Device address for the light sensor (change this if needed)
DEVICE_ADDRESS = 0x23  # Example address for BH1750

def read_light():
    # Read data from the light sensor
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x10)  # Command to start measurement
    light_level = (data[1] + (256 * data[0])) / 1.2  # Convert to Lux
    return light_level

try:
    while True:
        # Read light level from the sensor
        light = read_light()
        print(f"Light Level: {light:.2f} Lux")
        
        # Read from ADO pin
        ado_value = GPIO.input(ADO_PIN)
        print(f"ADO Pin Value: {'HIGH' if ado_value else 'LOW'}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
