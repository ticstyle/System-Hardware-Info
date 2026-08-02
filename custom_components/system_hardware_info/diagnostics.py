# custom_components/system_hardware_info/diagnostics.py
"""Diagnostics support for System Hardware Info."""

from __future__ import annotations

import os
import platform
from typing import Any

from homeassistant.core import HomeAssistant

from . import SystemHardwareConfigEntry
from .const import SYSFS_PATHS
from .sensor import (
    _get_bios_date,
    _get_boot_disk_model,
    _get_cpu_info,
    _get_cpu_max_freq,
    _get_hypervisor,
    _get_primary_mac,
    _get_total_ram,
    _read_sysfs_file,
)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: SystemHardwareConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    hardware_data: dict[str, str | None] = {}

    for key, path in SYSFS_PATHS.items():
        hardware_data[key] = await hass.async_add_executor_job(
            _read_sysfs_file, path
        )

    cpu_model, cpu_vendor, virt_capable = await hass.async_add_executor_job(
        _get_cpu_info
    )
    hardware_data["cpu_model"] = cpu_model
    hardware_data["cpu_vendor"] = cpu_vendor
    hardware_data["hardware_virt"] = virt_capable
    hardware_data["bios_date"] = await hass.async_add_executor_job(_get_bios_date)
    hardware_data["cpu_max_freq"] = await hass.async_add_executor_job(_get_cpu_max_freq)
    hardware_data["kernel_version"] = platform.release()
    hardware_data["cpu_cores"] = str(os.cpu_count())
    hardware_data["cpu_arch"] = platform.machine()
    hardware_data["total_ram"] = await hass.async_add_executor_job(_get_total_ram)
    hardware_data["hypervisor"] = await hass.async_add_executor_job(_get_hypervisor)
    hardware_data["boot_disk_model"] = await hass.async_add_executor_job(
        _get_boot_disk_model
    )
    hardware_data["primary_mac"] = await hass.async_add_executor_job(_get_primary_mac)

    return {
        "entry_id": entry.entry_id,
        "domain": entry.domain,
        "hardware": hardware_data,
    }
