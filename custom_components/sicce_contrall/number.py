"""Speed/setpoint entities exposed by ContrAll."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity


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


class SiccePumpSpeed(SicceEntity, NumberEntity):
    """Configured upper speed displayed by the ContrAll pump control."""

    _attr_native_min_value = 5
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, key: str) -> None:
        super().__init__(coordinator, key, "Pump speed", "mdi:pump")

    @property
    def native_value(self):
        return self.coordinator.pump_speed

    @property
    def available(self) -> bool:
        return super().available and self.native_value is not None

    async def async_set_native_value(self, value_: float) -> None:
        await self.coordinator.async_set_pump_speed(value_)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for coordinator in entry.runtime_data.coordinators.values():
        data = coordinator.data or {}
        if coordinator.pump_speed is not None:
            key = next((key for key in ("power", "current_power", "speed") if type(data.get(key)) in (int, float)), "power")
            entities.append(SiccePumpSpeed(coordinator, key))
        for key, name in (("eco_speed", "Eco speed"),
                          ("pause_speed", "Pause speed")):
            if isinstance(data.get(key), (int, float)):
                entities.append(SiccePercentNumber(coordinator, key, name))
    async_add_entities(entities)
