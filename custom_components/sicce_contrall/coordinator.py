"""Data coordinator for Sicce cloud devices."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SicceApiError, SicceClient
from .const import DOMAIN, UPDATE_INTERVAL


def device_id(data: dict[str, Any]) -> str | None:
    value = data.get("id", data.get("device_id", data.get("mac", data.get("serial"))))
    return str(value) if value is not None else None


class SicceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass, client: SicceClient, initial: dict[str, Any]) -> None:
        self.client = client
        self.device_id = device_id(initial)
        super().__init__(hass, logging.getLogger(__name__), name=DOMAIN,
                         update_interval=UPDATE_INTERVAL)
        self.data = initial

    async def _async_update_data(self) -> dict[str, Any]:
        if not self.device_id:
            raise UpdateFailed("ContrAll device has no stable id")
        try:
            settings = await self.client.async_get_settings(self.device_id)
        except SicceApiError as err:
            raise UpdateFailed(str(err)) from err
        return {**self.data, **settings}
