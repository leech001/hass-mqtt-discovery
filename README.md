# HASS-MQTT-DISCOVERY

## Python class library for generating and sending data to the Home Assistant via MQTT (AutoDiscovery) of data from sensors and devices

### Install
```Python
from HaMqttDevice import *

mqtt_client = mqtt.Client("user")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set('user', 'pass')
mqtt_client.connect("mqtt.mqtt.ru", 1883, 60)
mqtt_client.loop_forever()
```
### Binary sensor
```Python
HA_alarm = MqttBinary(mqtt_client, 'MotoBoard alarm', 'mdi:alarm-light')
HA_alarm.send(1)
```

### Sensor
```Python
HA_uptime = MqttSensor(mqtt_client, 'MotoBoard uptime', 'ms', 'mdi:camera-timer')
HA_uptime.send(123)
```

### Device tracker
```Python
HA_gps = MqttTracker(mqtt_client, 'MotoBoard GPS')
HA_gps.send(55.5, 37.5, 0)
```
