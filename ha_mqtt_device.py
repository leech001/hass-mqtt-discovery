import json

import paho.mqtt.client as mqtt


class Sensor:
    def __init__(self, client: mqtt.Client, name, unit_of_measurement, icon):
        self.client = client
        self.name = name
        self.unique_id = self.name.replace(" ", "_").lower()
        self.unit_of_measurement = unit_of_measurement
        self.icon = icon
        self.topic = f"homeassistant/sensor/{self.unique_id}"
        self._send_config()

    def _send_config(self):
        _config = {
            "~": self.topic,
            "name": self.name,
            "unique_id": self.unique_id,
            "stat_t": "~/state",
            "unit_of_measurement": self.unit_of_measurement,
            "icon": self.icon,
        }
        self.client.publish(f"{self.topic}/config", json.dumps(_config))

    def send(self, value):
        self.client.publish(f"{self.topic}/state", str(value))


class Tracker:
    def __init__(self, client: mqtt.Client, name):
        self.client = client
        self.name = name
        self.unique_id = self.name.replace(" ", "_").lower()
        self.topic = f"homeassistant/device_tracker/{self.unique_id}"
        self._send_config()

    def _send_config(self):
        _config = {
            "~": self.topic,
            "name": self.name,
            "unique_id": self.unique_id,
            "stat_t": "~/state",
            "json_attr_t": "~/attributes",
            "payload_home": "home",
            "payload_not_home": "not_home",
        }
        self.client.publish(f"{self.topic}/config", json.dumps(_config))

    def send(self, latitude, longitude, gps_accuracy):
        _payload = {
            "latitude": latitude,
            "longitude": longitude,
            "gps_accuracy": gps_accuracy,
        }
        self.client.publish(f"{self.topic}/attributes", json.dumps(_payload))


class Binary:
    def __init__(self, client: mqtt.Client, name, icon):
        self.client = client
        self.name = name
        self.unique_id = self.name.replace(" ", "_").lower()
        self.topic = f"homeassistant/binary_sensor/{self.unique_id}"
        self.icon = icon
        self._send_config()

    def _send_config(self):
        _config = {
            "~": self.topic,
            "name": self.name,
            "unique_id": self.unique_id,
            "stat_t": "~/state",
            "icon": self.icon,
        }
        self.client.publish(f"{self.topic}/config", json.dumps(_config))

    def send(self, value):
        self.client.publish(f"{self.topic}/state", str(value))
