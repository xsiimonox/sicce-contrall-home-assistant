"""Register the Sicce Studio panel in Home Assistant's sidebar."""
from __future__ import annotations

from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.panel_custom import async_register_panel
from homeassistant.core import HomeAssistant

from .const import DOMAIN, INTEGRATION_VERSION

PANEL_PATH = "sicce-studio"
STATIC_PATH = "/sicce_contrall_panel"


async def async_register_studio_panel(hass: HomeAssistant) -> None:
    """Register the authenticated Studio panel once per HA session."""
    state = hass.data.setdefault(DOMAIN, {})
    if not state.get("studio_static_registered"):
        await hass.http.async_register_static_paths([
            StaticPathConfig(
                STATIC_PATH,
                str(Path(__file__).parent / "panel"),
                False,
            )
        ])
        state["studio_static_registered"] = True

    if PANEL_PATH not in hass.data.get(frontend.DATA_PANELS, {}):
        await async_register_panel(
            hass,
            frontend_url_path=PANEL_PATH,
            webcomponent_name="sicce-studio-panel",
            sidebar_title="Sicce Studio",
            sidebar_icon="mdi:water-sync",
            module_url=f"{STATIC_PATH}/sicce-studio.js?v={INTEGRATION_VERSION}",
            require_admin=True,
            embed_iframe=False,
        )
