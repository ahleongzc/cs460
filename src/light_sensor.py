import smbus
import time

# I2C pins and device address
SDA_PIN = 24
SDA_PIN = 2 # SDA pin for I²C
SCL_PIN = 3  # SCL pin for I²C
DEVICE_ADDRESS = 0x23

def read_light():
    """Read the light level from the BH1750 light sensor."""
    bus = smbus.SMBus(1)  # Create I2C bus
    try:
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x10)  # Start measurement
        light_level = (data[1] + (256 * data[0])) / 1.2  # Convert to Lux
        return light_level
    except Exception as e:
        print(f"Error reading light sensor: {e}")
        return None
