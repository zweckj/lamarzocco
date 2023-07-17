"""Binary Sensor platform for La Marzocco espresso machines."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .const import (
    ATTR_MAP_BREW_ACTIVE,
    ATTR_MAP_WATER_RESERVOIR,
    BREW_ACTIVE,
    DOMAIN,
    ENTITY_CLASS,
    ENTITY_ICON,
    ENTITY_MAP,
    ENTITY_NAME,
    ENTITY_TAG,
    ENTITY_TYPE,
    CONF_USE_WEBSOCKET,
    MODEL_GS3_AV,
    MODEL_GS3_MP,
    MODEL_LM,
    MODEL_LMU,
    TYPE_BREW_ACTIVE,
    TYPE_WATER_RESERVOIR_CONTACT,
    WATER_RESERVOIR_CONTACT,
)
from .entity_base import EntityBase
from .services import async_setup_entity_services

_LOGGER = logging.getLogger(__name__)

ENTITIES = {
    "water_reservoir": {
        ENTITY_TAG: WATER_RESERVOIR_CONTACT,
        ENTITY_NAME: "Water Reservoir",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_WATER_RESERVOIR,
            MODEL_GS3_MP: ATTR_MAP_WATER_RESERVOIR,
            MODEL_LM: ATTR_MAP_WATER_RESERVOIR,
            MODEL_LMU: ATTR_MAP_WATER_RESERVOIR
        },
        ENTITY_TYPE: TYPE_WATER_RESERVOIR_CONTACT,
        ENTITY_ICON: "mdi:water-well",
        ENTITY_CLASS: BinarySensorDeviceClass.PROBLEM,
    },
    "brew_active": {
        ENTITY_TAG: BREW_ACTIVE,
        ENTITY_NAME: "Brew Active",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_BREW_ACTIVE,
            MODEL_GS3_MP: ATTR_MAP_BREW_ACTIVE,
            MODEL_LM: ATTR_MAP_BREW_ACTIVE,
            MODEL_LMU: ATTR_MAP_BREW_ACTIVE
        },
        ENTITY_TYPE: TYPE_BREW_ACTIVE,
        ENTITY_ICON: "mdi:cup-water",
        ENTITY_CLASS: BinarySensorDeviceClass.RUNNING,
    }
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up binary sensor entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    use_websocket = config_entry.options.get(CONF_USE_WEBSOCKET, False)

    entities = []
    for sensor_type in ENTITIES:
        if coordinator.lm.model_name in ENTITIES[sensor_type][ENTITY_MAP]:
            if sensor_type == "brew_active" and not use_websocket:
                continue
            entities.append(
                LaMarzoccoBinarySensor(coordinator, sensor_type, hass, config_entry)
            )

    async_add_entities(entities)

    await async_setup_entity_services(coordinator.lm)


class LaMarzoccoBinarySensor(EntityBase, BinarySensorEntity):
    """Binary Sensor representing espresso machine water reservoir status."""

    def __init__(self, coordinator, sensor_type, hass, config_entry):
        """Initialize binary sensors"""
        super().__init__(coordinator, hass, sensor_type, ENTITIES, ENTITY_TYPE)

    @property
    def available(self):
        """Return if binary sensor is available."""
        entity = self._entities[self._object_id][ENTITY_TAG]
        return self._lm.current_status.get(self._get_key(entity)) is not None

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        state = self._lm.current_status.get(
            self._get_key(self._entities[self._object_id][ENTITY_TAG])
        )

        if self._entity_type == TYPE_WATER_RESERVOIR_CONTACT:
            # invert state for water reservoir
            state = not state

        return state

    @property
    def device_class(self):
        """Device class for binary sensor"""
        return self._entities[self._object_id][ENTITY_CLASS]
