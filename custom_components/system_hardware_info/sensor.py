# custom_components/system_hardware_info/sensor.py
"""Sensor platform for System Hardware Info."""

from __future__ import annotations

import os
from pathlib import Path

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from . import SystemHardwareConfigEntry
from .const import (
    DEFAULT_NAME,
    DOMAIN,
    KEY_BIOS_VERSION,
    KEY_BOARD_NAME,
    KEY_BOARD_VENDOR,
    KEY_CPU_MODEL,
    KEY_PRODUCT_NAME,
    KEY_SYS_VENDOR,
    MANUFACTURER,
    SYSFS_PATHS,
)

# Explicit names for each hardware attribute
SENSOR_NAMES: dict[str, str] = {
    KEY_BOARD_NAME: "Motherboard",
    KEY_BOARD_VENDOR: "Motherboard Vendor",
    KEY_BIOS_VERSION: "Motherboard BIOS version",
    KEY_SYS_VENDOR: "System Vendor",
    KEY_PRODUCT_NAME: "Product Name",
    KEY_CPU_MODEL: "CPU",
}


def _read_sysfs_file(path_str: str) -> str | None:
    """Safely read a single sysfs string line (blocking executor target)."""
    path = Path(path_str)
    if path.exists() and os.access(path, os.R_OK):
        try:
            val = path.read_text(encoding="utf-8").strip()
            return val if val else None
        except OSError:
            return None
    return None


def _get_cpu_model() -> str | None:
    """Read CPU model name from /proc/cpuinfo (blocking executor target)."""
    cpu_path = Path("/proc/cpuinfo")
    if cpu_path.exists() and os.access(cpu_path, os.R_OK):
        try:
            lines = cpu_path.read_text(encoding="utf-8").splitlines()
            for line in lines:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
        except OSError:
            return None
    return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SystemHardwareConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the System Hardware Info sensors."""
    sensors: list[SystemHardwareSensor] = []

    # Read sysfs files using executor to prevent event loop blocking
    for key, path in SYSFS_PATHS.items():
        val = await hass.async_add_executor_job(_read_sysfs_file, path)
        sensors.append(SystemHardwareSensor(entry, key, val))

    # Read CPU model using executor
    cpu_val = await hass.async_add_executor_job(_get_cpu_model)
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_MODEL, cpu_val))

    async_add_entities(sensors)


class SystemHardwareSensor(SensorEntity):
    """Representation of a System Hardware Info sensor."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        entry: SystemHardwareConfigEntry,
        sensor_key: str,
        initial_value: str | None,
    ) -> None:
        """Initialize the sensor."""
        self._attr_translation_key = sensor_key
        self._sensor_key = sensor_key

        normalized_key = slugify(sensor_key)
        self._attr_unique_id = f"{entry.entry_id}_{normalized_key}"
        self.entity_id = f"sensor.{DOMAIN}_{normalized_key}"

        self._attr_native_value = initial_value or "Unknown"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer=MANUFACTURER,
            model=DEFAULT_NAME,
        )

    @property
    def name(self) -> str | None:
        """Return the friendly name of the individual sensor."""
        return SENSOR_NAMES.get(self._sensor_key)
