"""Speed/setpoint entities exposed by ContrAll."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity, value


class SiccePercentNumber(SicceEntity, NumberEntity):
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, key: str, name: str) -> None:
        super().__init__(coordinator, key, name, "mdi:pump")

    @property
    def native_value(self):
        raw = (self.coordinator.data or {}).get(self._key)
        return float(raw) if isinstance(raw, (int, float)) else None

    async def async_set_native_value(self, value_: float) -> None:
        await self._set(self._key, int(value_))


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for coordinator in entry.runtime_data.coordinators.values():
        data = coordinator.data or {}
        for key, name in (("current_power", "Pump speed"), ("power", "Pump speed"),
                          ("speed", "Pump speed"), ("eco_speed", "Eco speed"),
                          ("pause_speed", "Pause speed")):
            if isinstance(data.get(key), (int, float)):
                entities.append(SiccePercentNumber(coordinator, key, name))
    async_add_entities(entities)
