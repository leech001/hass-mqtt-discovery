# HASS-MQTT-DISCOVERY

Python class library for generating and sending data to the Home Assistant via
MQTT (AutoDiscovery) of data from sensors and devices.

## Build and Install
### build wheel: 

    # from top folder: 
    pip install -e .
    flit build

### install wheel:
       
    # inside dist folder:
    pip install hass_mqtt_discovery

## Usage
```Python
from hass

mqtt_client = mqtt.Client("user")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("user", "pass")
mqtt_client.connect("mqtt.mqtt.ru", 1883, 60)
mqtt_client.loop_forever()
```

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

#### Component value read function

If the hardware sensor is used solely to publish to mqtt, the `Sensor` can fetch
the value by itself so keeping a reference to both the hardware and the mqtt
sensor is not required.

For example:

```python
inside_temperature_sensor.set_value_read_function(lambda: round(hardware_sensor.temperature, 2))
```

From here publishing to the mqtt server would be:

```python
inside_temperature_sensor.send()
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
