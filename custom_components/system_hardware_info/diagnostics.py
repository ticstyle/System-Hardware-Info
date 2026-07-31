# custom_components/system_hardware_info/diagnostics.py
"""Diagnostics support for System Hardware Info."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import SystemHardwareConfigEntry
from .const import SYSFS_PATHS
from .sensor import _get_cpu_model, _read_sysfs_file


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: SystemHardwareConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    hardware_data: dict[str, str | None] = {}

    for key, path in SYSFS_PATHS.items():
        hardware_data[key] = _read_sysfs_file(path)

    hardware_data["cpu_model"] = _get_cpu_model()

    return {
        "entry_id": entry.entry_id,
        "domain": entry.domain,
        "hardware": hardware_data,
    }
