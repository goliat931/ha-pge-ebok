import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the PGE eBOK sensor from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([PgeEbokSensor(coordinator, config_entry)], False)

class PgeEbokSensor(CoordinatorEntity, SensorEntity):
    """Klasa reprezentująca sensor salda PGE eBOK."""

    def __init__(self, coordinator, config_entry):
        """Inicjalizacja sensora."""
        super().__init__(coordinator)
        self._username = config_entry.data[CONF_USERNAME]
        self._attr_has_entity_name = True
        self._attr_name = "Saldo"
        self._attr_native_unit_of_measurement = "PLN"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_icon = "mdi:flash"
        self._attr_unique_id = f"pge_ebok_{self._username}"

    @property
    def native_value(self):
        """Zwraca obecny stan sensora."""
        return self.coordinator.data

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._username)},
            name=f"PGE eBOK {self._username}",
            manufacturer="PGE",
            model="eBOK",
        )
