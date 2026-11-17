"""Shared Sicce entity helpers."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def value(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if data.get(key) is not None:
            return data[key]
    return None


class SicceEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, key: str, name: str, icon: str | None = None) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.device_id}_{key}"
        self._attr_icon = icon
        data = coordinator.data or {}
        model = value(data, "model", "device_model", "type") or "ContrAll device"
        serial = value(data, "serial", "mac", "device_id", "id")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.device_id)}, name=value(data, "name", "device_name") or f"Sicce {model}",
            manufacturer="Sicce", model=str(model), serial_number=str(serial) if serial else None,
            sw_version=value(data, "firmware_version", "firmware", "fw_version"),
        )

    async def _set(self, key: str, setting: Any) -> None:
        await self.coordinator.client.async_set_setting(self.coordinator.device_id, key, setting)
        await self.coordinator.async_request_refresh()
