"""Support for a Duolingo data sensor."""
from custom_components.duolingo.entity import DuolingoEntity
from datetime import timedelta
import logging

import duolingo
import requests
import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

from .const import (
    CONF_USERNAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

ATTR_DUO_STREAK_LENGTH = "streak_length"
ATTR_DUO_STREAK_EXTENDED_TODAY = "streak_extended_today"


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([DuolinguistBinarySensor(coordinator, entry)])


class DuolinguistBinarySensor(DuolingoEntity, BinarySensorEntity):
    """Implementation of the Duolinguist binary sensor."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DOMAIN}_{self.coordinator.data.get(CONF_USERNAME)}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get("streak_extended_today", False)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            ATTR_DUO_STREAK_EXTENDED_TODAY: self.coordinator.data.get(
                "streak_extended_today", False
            ),
            ATTR_DUO_STREAK_LENGTH: self.coordinator.data.get("site_streak", "0"),
        }
        return attrs