"""Config flow: user supplies a ContrAll API bearer token."""
from __future__ import annotations

from hashlib import sha256

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SicceApiError, SicceClient
from .const import CONF_BASE_URL, CONF_EMAIL, CONF_PASSWORD, DEFAULT_BASE_URL, DOMAIN


class SicceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            base_url = user_input[CONF_BASE_URL].rstrip("/")
            try:
                client = await SicceClient.async_login(
                    async_get_clientsession(self.hass), base_url, user_input[CONF_EMAIL], user_input[CONF_PASSWORD],
                )
                devices = await client.async_get_devices()
            except SicceApiError:
                errors["base"] = "cannot_connect"
            else:
                email_hash = sha256(user_input[CONF_EMAIL].strip().lower().encode()).hexdigest()[:16]
                await self.async_set_unique_id(f"sicce-contrall-{email_hash}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"Sicce ContrAll ({len(devices)} devices)",
                                               data={CONF_BASE_URL: base_url, CONF_EMAIL: user_input[CONF_EMAIL],
                                                     CONF_PASSWORD: user_input[CONF_PASSWORD]})
        schema = vol.Schema({vol.Required(CONF_EMAIL): str, vol.Required(CONF_PASSWORD): str,
                             vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
