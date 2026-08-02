# custom_components/system_hardware_info/diagnostics.py
"""Diagnostics support for System Hardware Info."""

from __future__ import annotations

import os
import platform
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import SystemHardwareConfigEntry
from .const import SYSFS_PATHS
from .sensor import (
    _get_bios_date,
    _get_boot_disk_info,
    _get_boot_mode,
    _get_chassis_type,
    _get_cpu_info,
    _get_cpu_l3_cache,
    _get_cpu_max_freq,
    _get_gpu_model,
    _get_hypervisor,
    _get_pci_count,
    _get_primary_mac,
    _get_total_ram,
    _get_usable_ram,
    _read_sysfs_file,
)

# Redact serial numbers and MAC addresses in diagnostic logs
TO_REDACT = ["primary_mac", "motherboard_serial"]


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
    disk_val, bus_val = await hass.async_add_executor_job(_get_boot_disk_info)

    hardware_data["cpu_model"] = cpu_model
    hardware_data["cpu_vendor"] = cpu_vendor
    hardware_data["hardware_virt"] = virt_capable
    hardware_data["bios_date"] = await hass.async_add_executor_job(_get_bios_date)
    hardware_data["cpu_max_freq"] = await hass.async_add_executor_job(_get_cpu_max_freq)
    hardware_data["cpu_cache_l3"] = await hass.async_add_executor_job(_get_cpu_l3_cache)
    hardware_data["kernel_version"] = platform.release()
    hardware_data["boot_mode"] = await hass.async_add_executor_job(_get_boot_mode)
    hardware_data["cpu_cores"] = str(os.cpu_count())
    hardware_data["cpu_arch"] = platform.machine()
    hardware_data["total_ram"] = await hass.async_add_executor_job(_get_total_ram)
    hardware_data["usable_ram"] = await hass.async_add_executor_job(_get_usable_ram)
    hardware_data["hypervisor"] = await hass.async_add_executor_job(_get_hypervisor)
    hardware_data["boot_disk_model"] = disk_val
    hardware_data["disk_bus_type"] = bus_val
    hardware_data["primary_mac"] = await hass.async_add_executor_job(_get_primary_mac)
    hardware_data["pci_devices_count"] = await hass.async_add_executor_job(_get_pci_count)
    hardware_data["gpu_model"] = await hass.async_add_executor_job(_get_gpu_model)
    hardware_data["system_chassis"] = await hass.async_add_executor_job(_get_chassis_type)

    redacted_data = async_redact_data(hardware_data, TO_REDACT)

    return {
        "entry_id": entry.entry_id,
        "domain": entry.domain,
        "hardware": redacted_data,
    }
