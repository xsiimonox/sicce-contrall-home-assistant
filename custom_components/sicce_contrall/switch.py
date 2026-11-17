"""Pause and energy-saving controls."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity, value


class SiccePauseSwitch(SicceEntity, SwitchEntity):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "pause", "Pause", "mdi:pause-circle")

    @property
    def is_on(self):
        return bool(value(self.coordinator.data or {}, "pause", "paused", "is_paused", "feed_mode"))

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.client.async_set_pause(self.coordinator.device_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.async_set_pause(self.coordinator.device_id, False)
        await self.coordinator.async_request_refresh()


class SicceBooleanSwitch(SicceEntity, SwitchEntity):
    def __init__(self, coordinator, key: str, name: str) -> None:
        super().__init__(coordinator, key, name, "mdi:leaf")

    @property
    def is_on(self):
        return bool((self.coordinator.data or {}).get(self._key))

    async def async_turn_on(self, **kwargs) -> None:
        await self._set(self._key, True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._set(self._key, False)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for coordinator in entry.runtime_data.coordinators.values():
        data = coordinator.data or {}
        if any(key in data for key in ("pause", "paused", "is_paused", "feed_mode")):
            entities.append(SiccePauseSwitch(coordinator))
        for key, name in (("eco", "Eco mode"), ("eco_enabled", "Eco mode"),
                          ("half_power", "Half power")):
            if isinstance(data.get(key), bool):
                entities.append(SicceBooleanSwitch(coordinator, key, name))
    async_add_entities(entities)
