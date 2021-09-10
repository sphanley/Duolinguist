"""Constants for integration_blueprint."""
# Base component constants
NAME = "Duolinguist"
DOMAIN = "duolingo"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = (
    "This integration is not affiliated with or endorsed by Duolingo, Inc. in any way."
)
ISSUE_URL = "https://github.com/sphanley/duolinguist/issues"

# Icons
ICON = "mdi:format-quote-close"

# Platforms
BINARY_SENSOR = "binary_sensor"
PLATFORMS = [BINARY_SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
