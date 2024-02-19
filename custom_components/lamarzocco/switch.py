"""Switch platform for La Marzocco espresso machines."""

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from lmcloud.const import BoilerType

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import LaMarzoccoMachineUpdateCoordinator
from .entity import LaMarzoccoEntity, LaMarzoccoEntityDescription


@dataclass(frozen=True, kw_only=True)
class LaMarzoccoSwitchEntityDescription(
    LaMarzoccoEntityDescription,
    SwitchEntityDescription,
):
    """Description of a La Marzocco Switch."""

    control_fn: Callable[
        [LaMarzoccoMachineUpdateCoordinator, bool], Coroutine[Any, Any, bool]
    ]
    is_on_fn: Callable[[LaMarzoccoMachineUpdateCoordinator], bool]


ENTITIES: tuple[LaMarzoccoSwitchEntityDescription, ...] = (
    LaMarzoccoSwitchEntityDescription(
        key="main",
        translation_key="main",
        name=None,
        control_fn=lambda coordinator, state: coordinator.device.set_power(
            state, coordinator.async_get_ble_device()
        ),
        is_on_fn=lambda coordinator: coordinator.device.config.turned_on,
    ),
    LaMarzoccoSwitchEntityDescription(
        key="auto_on_off",
        translation_key="auto_on_off",
        control_fn=lambda coordinator,
        enabled: coordinator.device.enable_schedule_globally(enabled),
        is_on_fn=lambda coordinator: coordinator.device.config.auto_on_off_schedule.enabled,
        entity_category=EntityCategory.CONFIG,
    ),
    LaMarzoccoSwitchEntityDescription(
        key="steam_boiler_enable",
        translation_key="steam_boiler",
        control_fn=lambda coordinator, state: coordinator.device.set_steam(
            state, coordinator.async_get_ble_device()
        ),
        is_on_fn=lambda coordinator: coordinator.device.config.boilers[
            BoilerType.STEAM
        ].enabled,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        LaMarzoccoSwitchEntity(coordinator, description)
        for description in ENTITIES
        if description.supported_fn(coordinator)
    )


class LaMarzoccoSwitchEntity(LaMarzoccoEntity, SwitchEntity):
    """Switches representing espresso machine power, prebrew, and auto on/off."""

    entity_description: LaMarzoccoSwitchEntityDescription

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn device on."""
        await self.entity_description.control_fn(self.coordinator, True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn device off."""
        await self.entity_description.control_fn(self.coordinator, False)
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return self.entity_description.is_on_fn(self.coordinator)
