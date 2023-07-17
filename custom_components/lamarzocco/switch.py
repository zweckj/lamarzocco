"""Switch platform for La Marzocco espresso machines."""

import logging

from homeassistant.components.switch import SwitchEntity

from .const import (
    ATTR_MAP_AUTO_ON_OFF,
    ATTR_MAP_MAIN_GS3_AV,
    ATTR_MAP_MAIN_GS3_MP,
    ATTR_MAP_MAIN_LM,
    ATTR_MAP_STEAM_BOILER_ENABLE,
    ATTR_MAP_PREBREW_GS3_AV,
    ATTR_MAP_PREBREW_LM,
    ATTR_MAP_PREINFUSION_GS3_AV,
    ATTR_MAP_PREINFUSION_LM,
    AUTO,
    DOMAIN,
    ENABLED,
    ENABLE_PREBREWING,
    ENABLE_PREINFUSION,
    ENTITY_FUNC,
    ENTITY_ICON,
    ENTITY_MAP,
    ENTITY_NAME,
    ENTITY_TAG,
    ENTITY_TYPE,
    GLOBAL,
    MODEL_GS3_AV,
    MODEL_GS3_MP,
    MODEL_LM,
    MODEL_LMU,
    POWER,
    STEAM_BOILER_ENABLE,
    TYPE_AUTO_ON_OFF,
    TYPE_MAIN,
    TYPE_PREBREW,
    TYPE_PREINFUSION,
    TYPE_STEAM_BOILER_ENABLE,
)

from .entity_base import EntityBase
from .services import async_setup_entity_services, call_service

_LOGGER = logging.getLogger(__name__)

ENTITIES = {
    "main": {
        ENTITY_TAG: POWER,
        ENTITY_NAME: "Main",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_MAIN_GS3_AV,
            MODEL_GS3_MP: ATTR_MAP_MAIN_GS3_MP,
            MODEL_LM: ATTR_MAP_MAIN_LM,
            MODEL_LMU: ATTR_MAP_MAIN_LM,
        },
        ENTITY_TYPE: TYPE_MAIN,
        ENTITY_ICON: "mdi:coffee-maker",
        ENTITY_FUNC: "set_power",
    },
    "auto_on_off": {
        ENTITY_TAG: (GLOBAL, AUTO),
        ENTITY_NAME: "Auto On Off",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_AUTO_ON_OFF,
            MODEL_GS3_MP: ATTR_MAP_AUTO_ON_OFF,
            MODEL_LM: ATTR_MAP_AUTO_ON_OFF,
            MODEL_LMU: ATTR_MAP_AUTO_ON_OFF
        },
        ENTITY_TYPE: TYPE_AUTO_ON_OFF,
        ENTITY_ICON: "mdi:alarm",
        ENTITY_FUNC: "set_auto_on_off_global",
    },
    "prebrew": {
        ENTITY_TAG: ENABLE_PREBREWING,
        ENTITY_NAME: "Prebrew",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_PREBREW_GS3_AV,
            MODEL_LM: ATTR_MAP_PREBREW_LM,
            MODEL_LMU: ATTR_MAP_PREBREW_LM,
        },
        ENTITY_TYPE: TYPE_PREBREW,
        ENTITY_ICON: "mdi:location-enter",
        ENTITY_FUNC: "set_prebrewing_enable",
    },
    "preinfusion": {
        ENTITY_TAG: ENABLE_PREINFUSION,
        ENTITY_NAME: "Preinfusion",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_PREINFUSION_GS3_AV,
            MODEL_LM: ATTR_MAP_PREINFUSION_LM,
            MODEL_LMU: ATTR_MAP_PREINFUSION_LM,
        },
        ENTITY_TYPE: TYPE_PREINFUSION,
        ENTITY_ICON: "mdi:location-enter",
        ENTITY_FUNC: "set_preinfusion_enable",
    },
    "steam_boiler_enable": {
        ENTITY_TAG: STEAM_BOILER_ENABLE,
        ENTITY_NAME: "Steam Boiler Enable",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_STEAM_BOILER_ENABLE,
            MODEL_GS3_MP: ATTR_MAP_STEAM_BOILER_ENABLE,
            MODEL_LM: ATTR_MAP_STEAM_BOILER_ENABLE,
            MODEL_LMU: ATTR_MAP_STEAM_BOILER_ENABLE,
        },
        ENTITY_TYPE: TYPE_STEAM_BOILER_ENABLE,
        ENTITY_ICON: "mdi:water-boiler",
        ENTITY_FUNC: "set_steam_boiler_enable",
    },
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up switch entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        LaMarzoccoSwitch(coordinator, switch_type, hass, config_entry)
        for switch_type in ENTITIES
        if coordinator.lm.model_name in ENTITIES[switch_type][ENTITY_MAP]
    )

    await async_setup_entity_services(coordinator.lm)


class LaMarzoccoSwitch(EntityBase, SwitchEntity):
    """Switches representing espresso machine power, prebrew, and auto on/off."""

    def __init__(self, coordinator, switch_type, hass, config_entry):
        """Initialise switches."""
        super().__init__(coordinator, hass, switch_type, ENTITIES, ENTITY_TYPE)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn device on."""
        await call_service(
            getattr(self._lm, self._entities[self._object_id][ENTITY_FUNC]), True
        )
        await self._update_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn device off."""
        await call_service(
            getattr(self._lm, self._entities[self._object_id][ENTITY_FUNC]), False
        )
        await self._update_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return self._lm.current_status.get(
            self._get_key(self._entities[self._object_id][ENTITY_TAG]), False
        ) in [True, ENABLED]
