"""Sensor platform for La Marzocco espresso machines."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from lmcloud.const import LaMarzoccoModel

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import LaMarzoccoEntity, LaMarzoccoEntityDescription
from .lm_client import LaMarzoccoClient

ATTR_MAP_DRINK_STATS_GS3_AV = [
    "drinks_k1",
    "drinks_k2",
    "drinks_k3",
    "drinks_k4",
    "continuous",
    "total_coffee",
    "total_flushing",
]

ATTR_MAP_DRINK_STATS_GS3_MP_LM = ["drinks_k1", "total_flushing", "total_coffee"]

@dataclass(frozen=True, kw_only=True)
class LaMarzoccoSensorEntityDescription(
    SensorEntityDescription,
    LaMarzoccoEntityDescription,
):
    """Description of an La Marzocco Sensor."""
    available_fn: Callable[[LaMarzoccoClient], bool]
    value_fn: Callable[[LaMarzoccoClient], float | int]
    extra_attributes: dict[str, Any] = field(default_factory=dict)


ENTITIES: tuple[LaMarzoccoSensorEntityDescription, ...] = (
    LaMarzoccoSensorEntityDescription(
        key="drink_stats",
        translation_key="drink_stats",
        icon="mdi:chart-line",
        native_unit_of_measurement="drinks",
        state_class=SensorStateClass.MEASUREMENT,
        available_fn=lambda client: all(
            client.current_status.get(p) is not None
            for p in ("drinks_k1", "total_flushing")
        ),
        value_fn=lambda client: sum(
            client.current_status.get(p, 0) for p in ("drinks_k1", "total_flushing")
        ),
        entity_category=EntityCategory.DIAGNOSTIC,
        extra_attributes={
            LaMarzoccoModel.GS3_AV: ATTR_MAP_DRINK_STATS_GS3_AV,
            LaMarzoccoModel.GS3_MP: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
            LaMarzoccoModel.LINEA_MINI: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
            LaMarzoccoModel.LINEA_MICRA: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
        },
    ),
    LaMarzoccoSensorEntityDescription(
        key="shot_timer",
        translation_key="shot_timer",
        icon="mdi:timer",
        native_unit_of_measurement="s",
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
        available_fn=lambda client: client.current_status.get("brew_active_duration")
        is not None,
        value_fn=lambda client: client.current_status.get("brew_active_duration", 0),
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        LaMarzoccoSensorEntity(coordinator, hass, description)
        for description in ENTITIES
        if coordinator.data.model_name in description.supported_models
    )


class LaMarzoccoSensorEntity(LaMarzoccoEntity, SensorEntity):
    """Sensor representing espresso machine temperature data."""

    entity_description: LaMarzoccoSensorEntityDescription

    @property
    def available(self) -> bool:
        """Return if sensor is available."""
        return self.entity_description.available_fn(self._lm_client)

    @property
    def native_value(self) -> int | float:
        """State of the sensor."""
        return self.entity_description.value_fn(self._lm_client)
