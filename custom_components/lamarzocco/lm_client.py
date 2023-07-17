
import logging

from lmcloud import LMCloud

from .const import *
from homeassistant.components import bluetooth

_LOGGER = logging.getLogger(__name__)


class LaMarzoccoClient(LMCloud):
    """Keep data for La Marzocco entities."""

    def __init__(self, hass, hass_config):
        """Initialise the LaMarzocco entity data."""
        super().__init__()

        self._device_version = None
        self._hass_config = hass_config
        self.hass = hass
        self._brew_active = False

    @property
    def model_name(self) -> str:
        """Return model name."""
        if super().model_name not in MODELS:
            _LOGGER.error(
                f"Unsupported model, falling back to all entities and services: {super().model_name}"
            )
        return super().model_name if super().model_name in MODELS else MODEL_GS3_AV

    @property
    def true_model_name(self) -> str:
        """Return the model name from the cloud, even if it's not one we know about.  Used for display only."""
        return self.model_name if self.model_name in MODELS else self.model_name + " (Unknown)"

    @property
    def machine_name(self) -> str:
        """Return the name of the machine."""
        return self.machine_info[MACHINE_NAME]

    @property
    def serial_number(self) -> str:
        """Return serial number."""
        return self.machine_info[SERIAL_NUMBER]

    '''
    Initialization
    '''

    async def hass_init(self) -> None:

        init_bt = False
        bt_scanner = None
        # check if there are any bluetooth adapters to use
        count = bluetooth.async_scanner_count(self.hass, connectable=True)
        if count > 0:
            _LOGGER.debug("Found bluetooth adapters, initializing with bluetooth.")
            init_bt = True
            bt_scanner = bluetooth.async_get_scanner(self.hass)

        await self.init_with_local_api(
            self._hass_config,
            self._hass_config[HOST],
            port=DEFAULT_PORT_CLOUD,
            use_bluetooth=init_bt,
            bluetooth_scanner=bt_scanner)

        _LOGGER.debug(f"Model name: {self.model_name}")

    '''
    interface methods
    '''

    async def set_power(self, power_on) -> None:
        await self.get_hass_bt_client()
        await super().set_power(power_on)

    async def set_steam_boiler_enable(self, enable) -> None:
        await self.get_hass_bt_client()
        await self.set_steam(enable)

    async def set_preinfusion_enable(self, enable) -> None:
        await self.set_preinfusion(enable)

    async def set_prebrewing_enable(self, enable) -> None:
        await self.set_prebrew(enable)

    async def set_auto_on_off_global(self, enable) -> None:
        await self.configure_schedule(enable, self.schedule)

    async def set_auto_on_off_enable(self, day_of_week, enable) -> None:
        await super().set_auto_on_off_enable(day_of_week, enable)

    async def set_auto_on_off_times(self, day_of_week, hour_on, minute_on, hour_off, minute_off) -> None:
        await self.set_auto_on_off(day_of_week, hour_on, minute_on, hour_off, minute_off)

    async def set_dose(self, key, pulses) -> None:
        await super().set_dose(key, pulse)

    async def set_dose_hot_water(self, seconds) -> None:
        await super().set_dose_hot_water(seconds)

    async def set_prebrew_times(self, key, seconds_on, seconds_off) -> None:
        await self.configure_prebrew(prebrewOnTime=seconds_on * 1000, prebrewOffTime=seconds_off * 1000)

    async def set_preinfusion_time(self, key, seconds) -> None:
        await self.configure_prebrew(prebrewOnTime=0, prebrewOffTime=seconds * 1000)

    async def set_start_backflush(self) -> None:
        await self.start_backflush()

    async def set_coffee_temp(self, temp) -> None:
        await self.get_hass_bt_client()
        await super().set_coffee_temp(temp)

    async def set_steam_temp(self, temp) -> None:
        possible_temps = [126, 128, 131]
        temp = min(possible_temps, key=lambda x: abs(x - temp))
        await self.get_hass_bt_client()
        await super().set_steam_temp(temp)

    async def get_hass_bt_client(self) -> None:
        # according to HA best practices, we should not reuse the same client
        # get a new BLE device from hass and init a new Bleak Client with it
        if self._lm_bluetooth:
            ble_device = bluetooth.async_ble_device_from_address(self.hass,
                                                                 self._lm_bluetooth._address,
                                                                 connectable=True)
            await self._lm_bluetooth.new_bleak_client_from_ble_device(ble_device)
