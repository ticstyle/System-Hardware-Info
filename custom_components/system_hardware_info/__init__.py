# custom_components/system_hardware_info/__init__.py
"""The System Hardware Info integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type SystemHardwareConfigEntry = ConfigEntry[None]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SystemHardwareConfigEntry,
) -> bool:
    """Set up System Hardware Info from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SystemHardwareConfigEntry,
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: SystemHardwareConfigEntry,
    device_entry: dr.DeviceEntry,
) -> bool:
    """Remove a device entry when deleted by the user in the UI."""
    return True
