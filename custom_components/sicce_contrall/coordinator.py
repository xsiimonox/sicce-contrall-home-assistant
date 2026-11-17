"""Data coordinator for Sicce cloud devices."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SicceApiError, SicceClient
from .const import DOMAIN, UPDATE_INTERVAL
from .pump import speed_percent


def device_id(data: dict[str, Any]) -> str | None:
    value = data.get("id", data.get("device_id", data.get("mac", data.get("serial"))))
    return str(value) if value is not None else None


class SicceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass, client: SicceClient, initial: dict[str, Any]) -> None:
        self.client = client
        self.device_id = device_id(initial)
        self._initial = initial
        self.pump_speed = None
        self._speed_lock = asyncio.Lock()
        super().__init__(hass, logging.getLogger(__name__), name=DOMAIN,
                         update_interval=UPDATE_INTERVAL)
        self.data = initial

    async def _async_update_data(self) -> dict[str, Any]:
        if not self.device_id:
            raise UpdateFailed("ContrAll device has no stable id")
        try:
            try:
                settings = await self._async_get_device()
            except SicceApiError as err:
                if err.status != 404:
                    raise
                self.pump_speed = None
                for device in await self.client.async_get_devices():
                    if device_id(device) == self.device_id:
                        return device
                raise SicceApiError("ContrAll device is no longer in the account") from err
        except SicceApiError as err:
            raise UpdateFailed(str(err)) from err
        self.pump_speed = speed_percent(settings)
        return {**self._initial, **settings}

    async def _async_get_device(self) -> dict[str, Any]:
        device = await self.client.async_get_device(self.device_id)
        # List metadata can identify the model. Speed and program fields must
        # come from the fresh detail response.
        for key in ("device_model_id", "is_whale"):
            if key in self._initial:
                device.setdefault(key, self._initial[key])
        return device

    async def async_set_pump_speed(self, percent: float) -> None:
        async with self._speed_lock:
            current = await self._async_get_device()
            target = await self.client.async_set_speed(self.device_id, current, percent)
            for attempt in range(5):
                await self.async_refresh()
                if self.last_update_success and self.pump_speed == target:
                    return
                if attempt < 4:
                    await asyncio.sleep(2)
            raise SicceApiError("ContrAll accepted the command but did not report the requested speed")
