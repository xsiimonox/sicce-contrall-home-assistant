"""ContrAll operating-mode selector."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity


class SicceModeSelect(SicceEntity, SelectEntity):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "mode", "Mode", "mdi:wave")
        data = coordinator.data or {}
        choices = data.get("available_modes", data.get("modes", []))
        self._attr_options = [str(item) for item in choices] if isinstance(choices, list) else []

    @property
    def current_option(self):
        value = (self.coordinator.data or {}).get("mode")
        return str(value) if value is not None else None

    async def async_select_option(self, option: str) -> None:
        await self._set("mode", option)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = [SicceModeSelect(c) for c in entry.runtime_data.coordinators.values()
                if isinstance((c.data or {}).get("available_modes", (c.data or {}).get("modes")), list)]
    async_add_entities(entities)
