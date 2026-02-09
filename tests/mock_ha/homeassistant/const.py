from enum import StrEnum


class Platform(StrEnum):
    BINARY_SENSOR = "binary_sensor"
    SENSOR = "sensor"
    CALENDAR = "calendar"
    DEVICE_TRACKER = "device_tracker"
    SWITCH = "switch"
    LIGHT = "light"


CONF_NAME = "name"
CONF_ENTITY_ID = "entity_id"
ATTR_ENTITY_ID = "entity_id"
