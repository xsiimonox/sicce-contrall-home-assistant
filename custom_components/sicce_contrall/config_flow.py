"""Config flow: user supplies a ContrAll API bearer token."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SicceApiError, SicceClient
from .const import CONF_BASE_URL, CONF_TOKEN, DEFAULT_BASE_URL, DOMAIN


class SicceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            base_url = user_input[CONF_BASE_URL].rstrip("/")
            client = SicceClient(async_get_clientsession(self.hass), base_url, user_input[CONF_TOKEN])
            try:
                devices = await client.async_get_devices()
            except SicceApiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"sicce-contrall-{user_input[CONF_TOKEN][-12:]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"Sicce ContrAll ({len(devices)} devices)",
                                               data={CONF_BASE_URL: base_url, CONF_TOKEN: user_input[CONF_TOKEN]})
        schema = vol.Schema({vol.Required(CONF_TOKEN): str,
                             vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
