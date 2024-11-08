import paho.mqtt.client as mqtt

mqtt_broker = "mqtt.eclipse.org"  # MQTT broker (change if necessary)
mqtt_port = 1883
mqtt_topic = "home/motion"

def send_message(message):
    """Send a message via MQTT."""
    client = mqtt.Client()
    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        client.publish(mqtt_topic, message)
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")
    finally:
        client.disconnect()
