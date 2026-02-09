def async_get(hass):
    return type("EntityRegistry", (), {"async_get": lambda *args: None})()
