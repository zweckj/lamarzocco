"""Switch platform for La Marzocco espresso machines."""

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any, Generic

from lmcloud.const import BoilerType
from lmcloud.lm_machine import LaMarzoccoMachine
from lmcloud.models import LaMarzoccoMachineConfig

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import _DeviceT
from .entity import LaMarzoccoEntity, LaMarzoccoEntityDescription, _ConfigT


@dataclass(frozen=True, kw_only=True)
class LaMarzoccoSwitchEntityDescription(
    LaMarzoccoEntityDescription,
    SwitchEntityDescription,
    Generic[_DeviceT, _ConfigT],
):
    """Description of a La Marzocco Switch."""

    control_fn: Callable[[_DeviceT, bool], Coroutine[Any, Any, bool]]
    is_on_fn: Callable[[_ConfigT], bool]


ENTITIES: tuple[LaMarzoccoSwitchEntityDescription, ...] = (
    LaMarzoccoSwitchEntityDescription[LaMarzoccoMachine, LaMarzoccoMachineConfig](
        key="main",
        translation_key="main",
        name=None,
        control_fn=lambda machine, state: machine.set_power(enabled=state),
        is_on_fn=lambda config: config.turned_on,
    ),
    LaMarzoccoSwitchEntityDescription[LaMarzoccoMachine, LaMarzoccoMachineConfig](
        key="steam_boiler_enable",
        translation_key="steam_boiler",
        control_fn=lambda machine, state: machine.set_steam(enabled=state),
        is_on_fn=lambda config: config.boilers[BoilerType.STEAM].enabled,
    ),
    LaMarzoccoSwitchEntityDescription[LaMarzoccoMachine, LaMarzoccoMachineConfig](
        key="standby_enabled",
        translation_key="standby_enabled",
        entity_category=EntityCategory.CONFIG,
        control_fn=lambda machine, state: machine.set_smart_standby(
            enabled=state,
            mode=machine.config.smart_standby.mode,
            minutes=machine.config.smart_standby.minutes,
        ),
        is_on_fn=lambda config: config.smart_standby.enabled,
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
        await self.entity_description.control_fn(self.coordinator.device, True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn device off."""
        await self.entity_description.control_fn(self.coordinator.device, False)
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return self.entity_description.is_on_fn(self.coordinator.device.config)
