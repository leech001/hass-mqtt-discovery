import json
import yaml

import paho.mqtt.client as mqtt


DISCOVERY_PREFIX = "homeassistant"


class Device(dict):
    def __init__(self, identifiers, name, sw_version, model, manufacturer):
        super().__init__()

        self.name = name

        self["identifiers"] = identifiers
        self["name"] = name
        self["sw_version"] = sw_version
        self["model"] = model
        self["manufacturer"] = manufacturer

    @staticmethod
    def from_config(config_yaml_path):
        with open(config_yaml_path) as file:
            device_config = yaml.safe_load(file)
            device = Device(**device_config)
            return device


class Component:
    def __init__(self, name):
        self.component = name


class Sensor(Component):
    def __init__(
        self,
        client: mqtt.Client,
        name,
        parent_device,
        unit_of_measurement,
        icon=None,
        topic_parent_level="",
    ):
        super().__init__("sensor")

        self.client = client
        self.name = name
        self.parent_device = parent_device
        self.object_id = self.name.replace(" ", "_").lower()
        self.unit_of_measurement = unit_of_measurement
        self.icon = icon
        self.topic_parent_level = topic_parent_level
        self.topic = f"{self.parent_device.name}/{self.component}/{self.topic_parent_level}/{self.object_id}"
        self._send_config()

    def _send_config(self):
        _config = {
            "~": self.topic,
            "name": self.name,
            "state_topic": "~/state",
            "unit_of_measurement": self.unit_of_measurement,
            "device": self.parent_device,
        }

        if self.icon:
            _config["icon"] = self.icon

        self.client.publish(
            f"{DISCOVERY_PREFIX}/{self.component}/{self.parent_device.name}/{self.object_id}/config",
            json.dumps(_config),
        ).wait_for_publish()

    def send(self, value):
        self.client.publish(f"{self.topic}/state", str(value))


class Tracker:
    def __init__(self, client: mqtt.Client, name):
        self.client = client
        self.name = name
        self.unique_id = self.name.replace(" ", "_").lower()
        self.topic = f"{DISCOVERY_PREFIX}/device_tracker/{self.unique_id}"
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
        self.topic = f"{DISCOVERY_PREFIX}/binary_sensor/{self.unique_id}"
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
