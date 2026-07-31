# custom_components/system_hardware_info/config_flow.py
"""Config flow for System Hardware Info integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
)

from .const import DEFAULT_NAME, DOMAIN


class SystemHardwareInfoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for System Hardware Info."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={},
            )

        return self.async_show_form(step_id="user")

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle native UI reconfiguration."""
        if user_input is not None:
            return self.async_update_reload_and_abort(
                self._get_reconfigure_entry(),
                data={},
            )

        return self.async_show_form(step_id="reconfigure")
