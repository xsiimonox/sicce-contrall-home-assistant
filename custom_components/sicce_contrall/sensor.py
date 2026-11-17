"""Read-only telemetry from Sicce controllers."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity, value


class SicceSensor(SicceEntity, SensorEntity):
    def __init__(self, coordinator, key: str, name: str, unit=None, device_class=None, icon=None) -> None:
        super().__init__(coordinator, key, name, icon)
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self._key)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    definitions = (("temperature", "Temperature", "°C", SensorDeviceClass.TEMPERATURE, "mdi:thermometer"),
                   ("water_temperature", "Water temperature", "°C", SensorDeviceClass.TEMPERATURE, "mdi:thermometer-water"),
                   ("status", "Status", None, None, "mdi:information-outline"),
                   ("firmware_version", "Firmware", None, None, "mdi:chip"))
    for coordinator in entry.runtime_data.coordinators.values():
        data = coordinator.data or {}
        for key, name, unit, cls, icon in definitions:
            if data.get(key) is not None:
                entities.append(SicceSensor(coordinator, key, name, unit, cls, icon))
    async_add_entities(entities)
