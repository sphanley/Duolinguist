"""Support for a Duolingo data sensor."""
from datetime import timedelta
import logging

import duolingo
import requests
import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

ATTR_DUO_STREAK_LENGTH = "streak_length"
ATTR_DUO_STREAK_EXTENDED_TODAY = "streak_extended_today"

DEFAULT_NAME = "Duo"
DEFAULT_DEVICE_CLASS = "visible"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=900)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    try:
        duo_data = DuoData(username, password)
        await hass.async_add_executor_job(duo_data.update)

    except requests.exceptions.HTTPError as error:
        _LOGGER.error(error)
        return False

    async_add_devices([DuolinguistBinarySensor(duo_data, username, password)])


class DuolinguistBinarySensor(BinarySensorEntity):
    """Implementation of the Duolinguist binary sensor."""

    def __init__(self, duo_data, name, password):
        """Initialize the sensor."""
        self.duo_data = duo_data
        self._state = None
        self._name = name
        self._password = password

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.duo_data.streak_extended_today if self.duo_data else False

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return DEFAULT_DEVICE_CLASS

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.duo_data:
            attrs = {
                ATTR_DUO_STREAK_EXTENDED_TODAY: self.duo_data.streak_extended_today,
                ATTR_DUO_STREAK_LENGTH: self.duo_data.streak_length,
            }

            return attrs

    def update(self):
        """Get the latest data from Duolingo API and updates the states."""
        self.duo_data.update()


class DuoData:
    """Get data from the Duolingo API."""

    def __init__(self, username, password):
        """Initialize the data object."""
        self.streak_extended_today = None
        self.streak_length = None
        self._username = username
        self._password = password

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the Duolingo API."""
        try:
            duo = duolingo.Duolingo(self._username, self._password).get_streak_info()
            self.streak_extended_today = duo["streak_extended_today"]
            self.streak_length = duo["site_streak"]
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            _LOGGER.error("Unable to retrieve data")
            return False
