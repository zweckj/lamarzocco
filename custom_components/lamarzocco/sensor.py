"""Sensor platform for La Marzocco espresso machines."""

import logging

from .const import (
    ATTR_MAP_DRINK_STATS_GS3_AV,
    ATTR_MAP_DRINK_STATS_GS3_MP_LM,
    DOMAIN,
    DRINKS,
    ENTITY_CLASS,
    ENTITY_ICON,
    ENTITY_MAP,
    ENTITY_NAME,
    ENTITY_TAG,
    ENTITY_TYPE,
    ENTITY_UNITS,
    MODEL_GS3_AV,
    MODEL_GS3_MP,
    MODEL_LM,
    MODEL_LMU,
    TOTAL_FLUSHING,
    TYPE_DRINK_STATS,
)

from .entity_base import EntityBase
from .services import async_setup_entity_services

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity

_LOGGER = logging.getLogger(__name__)

ENTITIES = {
    "drink_stats": {
        ENTITY_TAG: [
            (DRINKS, "k1"),
            TOTAL_FLUSHING
        ],
        ENTITY_NAME: "Total Drinks",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_DRINK_STATS_GS3_AV,
            MODEL_GS3_MP: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
            MODEL_LM: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
            MODEL_LMU: ATTR_MAP_DRINK_STATS_GS3_MP_LM
        },
        ENTITY_TYPE: TYPE_DRINK_STATS,
        ENTITY_ICON: "mdi:coffee",
        ENTITY_CLASS: None,
        ENTITY_UNITS: "drinks",
    },
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        LaMarzoccoSensor(coordinator, sensor_type, hass, config_entry)
        for sensor_type in ENTITIES
        if coordinator.lm.model_name in ENTITIES[sensor_type][ENTITY_MAP]
    )

    await async_setup_entity_services(coordinator.lm)


class LaMarzoccoSensor(EntityBase, SensorEntity):
    """Sensor representing espresso machine temperature data."""

    def __init__(self, coordinator, sensor_type, hass, config_entry):
        """Initialize sensors"""
        super().__init__(coordinator, hass, sensor_type, ENTITIES, ENTITY_TYPE)

        self._attr_native_unit_of_measurement = self._entities[self._object_id][ENTITY_UNITS]
        self._attr_device_class = self._entities[self._object_id][ENTITY_CLASS]
        self._attr_state_class = STATE_CLASS_MEASUREMENT

    @property
    def available(self):
        """Return if sensor is available."""
        return all(
            self._lm.current_status.get(self._get_key(x)) is not None
            for x in self._entities[self._object_id][ENTITY_TAG]
        )

    @property
    def native_value(self):
        """State of the sensor."""
        entities = self._entities[self._object_id][ENTITY_TAG]
        return sum([self._lm.current_status.get(self._get_key(x), 0) for x in entities])
