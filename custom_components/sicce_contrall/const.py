"""Constants for the Sicce ContrAll integration."""
from datetime import timedelta

DOMAIN = "sicce_contrall"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_BASE_URL = "base_url"
DEFAULT_BASE_URL = "https://sicce.thingscloud.it/api"
UPDATE_INTERVAL = timedelta(seconds=30)
PLATFORMS = ("sensor", "number", "select", "switch", "button")

# These paths are present in ContrAll 2.33's production bundle.  Device
# payloads differ by product family, so field discovery deliberately happens
# at runtime rather than pretending every Sicce controller is a pump.
DEVICE_LIST_PATHS = ("/devices", "/user/devices", "/aquariums")
LOGIN_PATH = "/mobile/login"
SETTINGS_PATH = "/v2/settings"
PAUSE_PATH = "/v2/pauseDevice"
