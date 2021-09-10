"""DuolingoEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class DuolingoEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id