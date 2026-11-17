"""Refresh button."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry

from .entity import SicceEntity


class SicceRefreshButton(SicceEntity, ButtonEntity):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "refresh", "Refresh", "mdi:refresh")

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    async_add_entities([SicceRefreshButton(c) for c in entry.runtime_data.coordinators.values()])
