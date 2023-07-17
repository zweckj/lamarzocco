"""Base class for the La Marzocco entities."""

import asyncio
import logging

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ENTITY_ICON,
    ENTITY_MAP,
    ENTITY_NAME,
    UPDATE_DELAY
)

_LOGGER = logging.getLogger(__name__)


class EntityBase(CoordinatorEntity):
    """Common elements for all entities."""

    _attr_assumed_state = False
    _attr_entity_registry_enabled_default = True

    def __init__(self, coordinator, hass, object_id, entities, entity_type):
        super().__init__(coordinator)
        self._object_id = object_id
        self._hass = hass
        self._entities = entities
        self._entity_type = self._entities[self._object_id][entity_type]
        self._lm = self.coordinator.data

    @property
    def name(self):
        """Return the name of the switch."""
        return (
            f"{self._lm.machine_name} " + self._entities[self._object_id][ENTITY_NAME]
        )

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{self._lm.serial_number}_" + self._object_id

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return self._entities[self._object_id][ENTITY_ICON]

    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN, self._lm.serial_number)},
            "name": self._lm.machine_name,
            "manufacturer": "La Marzocco",
            "model": self._lm.true_model_name,
            "default_name": "La Marzocco " + self._lm.true_model_name,
            "sw_version": self._lm.firmware_version,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        def convert_value(k, v):
            """Convert boolean values to strings to improve display in Lovelace."""
            if isinstance(v, bool):
                v = str(v)
            return v

        data = self._lm.current_status
        attr = self._entities[self._object_id][ENTITY_MAP][self._lm.model_name]
        if attr is None:
            return {}

        map = [
            self._get_key(k) for k in attr
        ]

        return {k: convert_value(k, data[k]) for k in map if k in data}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._lm = self.coordinator.data
        self.async_write_ha_state()

    async def _update_ha_state(self):
        """ Write the intermediate value returned from the action to HA state before actually refreshing"""
        self.async_write_ha_state()
        # wait for a bit before getting a new state, to let the machine settle in to any state changes
        await asyncio.sleep(UPDATE_DELAY)
        await self.coordinator.async_request_refresh()

    def _get_key(self, k):
        """Construct tag name if needed."""
        if isinstance(k, tuple):
            k = "_".join(k)
        return k
