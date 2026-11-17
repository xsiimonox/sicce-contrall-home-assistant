"""Sicce ContrAll integration."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SicceClient
from .const import CONF_BASE_URL, CONF_TOKEN, DOMAIN, PLATFORMS
from .coordinator import SicceCoordinator, device_id


@dataclass
class SicceRuntimeData:
    coordinators: dict[str, SicceCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = SicceClient(async_get_clientsession(hass), entry.data[CONF_BASE_URL], entry.data[CONF_TOKEN])
    devices = await client.async_get_devices()
    coordinators: dict[str, SicceCoordinator] = {}
    for device in devices:
        identifier = device_id(device)
        if identifier is None:
            continue
        coordinator = SicceCoordinator(hass, client, device)
        await coordinator.async_config_entry_first_refresh()
        coordinators[identifier] = coordinator
    entry.runtime_data = SicceRuntimeData(coordinators)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
