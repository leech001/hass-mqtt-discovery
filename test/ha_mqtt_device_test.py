from hass_mqtt_discovery.hass_mqtt_device import Device


device = Device.from_config("example_device.yaml")
print(device)
