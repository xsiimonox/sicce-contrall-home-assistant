"""Small, defensive client for the Sicce ThingsCloud API."""
from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

from aiohttp import ClientResponseError, ClientSession
from homeassistant.exceptions import HomeAssistantError

from .const import DEVICE_LIST_PATHS, LOGIN_PATH, PAUSE_PATH, SETTINGS_PATH

_LOGGER = logging.getLogger(__name__)


class SicceApiError(HomeAssistantError):
    """The ContrAll cloud rejected a request or returned an unexpected reply."""


class SicceClient:
    """Authenticated client.  No password is retained by Home Assistant."""

    def __init__(self, session: ClientSession, base_url: str, token: str) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._details_path: str | None = None
        self._details_unavailable = False

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _request(
        self, method: str, path: str, payload: dict | None = None, *, authenticate: bool = True,
    ) -> Any:
        try:
            headers = self._headers if authenticate else {"Content-Type": "application/json", "Accept": "application/json"}
            request_kwargs = {"params": payload} if method == "GET" else {"json": payload}
            async with self._session.request(method, f"{self._base_url}{path}", headers=headers,
                                             timeout=20, **request_kwargs) as response:
                response.raise_for_status()
                return await response.json(content_type=None)
        except ClientResponseError as err:
            raise SicceApiError(f"Sicce API {method} {path}: HTTP {err.status}") from err
        except Exception as err:
            raise SicceApiError(f"Sicce API {method} {path}: {err}") from err

    @staticmethod
    def _token_from_login(reply: Any) -> str | None:
        """Extract the session token while accepting API response envelopes."""
        if not isinstance(reply, Mapping) or reply.get("result") is False:
            return None
        candidates = (reply, reply.get("data"), reply.get("user"))
        for candidate in candidates:
            if not isinstance(candidate, Mapping):
                continue
            for key in ("token", "access_token", "accessToken", "id_token", "idToken"):
                token = candidate.get(key)
                if isinstance(token, str) and token:
                    return token
        return None

    @classmethod
    async def async_login(cls, session: ClientSession, base_url: str, email: str, password: str) -> "SicceClient":
        """Create an authenticated client with ContrAll's verified mobile login.

        The endpoint and email/password body were checked against ContrAll 2.33
        with deliberately invalid credentials.  The password is never logged.
        """
        anonymous = cls(session, base_url, "")
        reply = await anonymous._request(
            "POST", LOGIN_PATH, {"email": email, "password": password}, authenticate=False,
        )
        token = cls._token_from_login(reply)
        if token is None:
            detail = reply.get("error") if isinstance(reply, Mapping) else None
            raise SicceApiError(str(detail or "Sicce account login failed"))
        return cls(session, base_url, token)

    @staticmethod
    def _devices(reply: Any) -> list[dict[str, Any]]:
        """Extract device records while preserving unknown product families."""
        if isinstance(reply, list):
            return [item for item in reply if isinstance(item, dict)]
        if not isinstance(reply, Mapping):
            return []
        for key in ("devices", "data", "items", "smart_systems", "aquariums"):
            value = reply.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [dict(reply)] if any(key in reply for key in ("id", "device_id", "mac")) else []

    async def async_get_devices(self) -> list[dict[str, Any]]:
        errors: list[str] = []
        for path in DEVICE_LIST_PATHS:
            try:
                devices = self._devices(await self._request("GET", path))
                if devices:
                    return devices
            except SicceApiError as err:
                errors.append(str(err))
        raise SicceApiError("Could not list ContrAll devices. " + "; ".join(errors))

    async def async_get_settings(self, device_id: str) -> dict[str, Any]:
        """Read details without treating an absent optional route as fatal.

        ContrAll accounts already return a device snapshot from the discovery
        endpoint.  Some controller/API combinations do not expose the old
        ``/v2/settings`` route at all (HTTP 404), so it must never prevent a
        device from being set up in Home Assistant.
        """
        if not self._details_unavailable:
            # A per-device REST resource is a common optional API shape.  Do
            # not probe a list of undocumented paths: each failed request
            # delays setup, and ``/v2/settings`` is known to be absent for at
            # least one current controller/API combination.
            paths = (self._details_path,) if self._details_path else (f"/devices/{device_id}",)
            for path in paths:
                if path is None:
                    continue
                try:
                    reply = await self._request("GET", path, {"device_id": device_id})
                except SicceApiError as err:
                    if "HTTP 404" not in str(err):
                        raise
                    continue
                if isinstance(reply, Mapping):
                    self._details_path = path
                    return dict(reply.get("data", reply))
            self._details_unavailable = True

        # The device list is confirmed to work during the config flow. Use its
        # latest matching item as a safe read-only fallback.
        for device in await self.async_get_devices():
            for key in ("id", "device_id", "mac", "serial"):
                if str(device.get(key)) == device_id:
                    return device
        raise SicceApiError(f"ContrAll device {device_id} is no longer in the account")

    async def async_set_setting(self, device_id: str, key: str, value: Any) -> None:
        await self._request("POST", SETTINGS_PATH, {"device_id": device_id, key: value})

    async def async_set_pause(self, device_id: str, paused: bool) -> None:
        await self._request("POST", PAUSE_PATH, {"device_id": device_id, "pause": paused})
