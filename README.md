# HASS-MQTT-DISCOVERY

Python class library for generating and sending data to the Home Assistant via MQTT (AutoDiscovery) of data from sensors and devices

## Install
```Python
from HaMqttDevice import *

mqtt_client = mqtt.Client("user")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("user", "pass")
mqtt_client.connect("mqtt.mqtt.ru", 1883, 60)
mqtt_client.loop_forever()
```

## Usage

### Sensor
```Python
example_device = Device.from_config("example_device.yaml")

inside_temperature_sensor = Sensor(
    mqtt_client,
    "Temperature 1",
    parent_device=example_device,
    unit_of_measurement="°C",
    topic_parent_level="inside",
)

outside_temperature_sensor = Sensor(
    mqtt_client,
    "Temperature 2",
    parent_device=example_device,
    unit_of_measurement="°C",
    topic_parent_level="outside",
)

inside_temperature_sensor.send(22)
outside_temperature_sensor.send(5)
```

### Device tracker
```Python
HA_gps = Tracker(mqtt_client, "MotoBoard GPS")
HA_gps.send(55.5, 37.5, 0)
```

### Binary sensor
```Python
HA_alarm = Binary(mqtt_client, "MotoBoard alarm", "mdi:alarm-light")
HA_alarm.send(1)
```
