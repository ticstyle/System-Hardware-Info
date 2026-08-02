# custom_components/system_hardware_info/sensor.py
"""Sensor platform for System Hardware Info."""

from __future__ import annotations

import os
from pathlib import Path
import platform

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from . import SystemHardwareConfigEntry
from .const import (
    DEFAULT_NAME,
    DOMAIN,
    KEY_BOOT_DISK,
    KEY_CPU_ARCH,
    KEY_CPU_CORES,
    KEY_CPU_MODEL,
    KEY_HYPERVISOR,
    KEY_PRIMARY_MAC,
    KEY_TOTAL_RAM,
    MANUFACTURER,
    SYSFS_PATHS,
)


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


def _get_total_ram() -> str | None:
    """Calculate total physical installed RAM in GB."""
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        if pages > 0 and page_size > 0:
            ram_gb = round((pages * page_size) / (1024**3), 2)
            return f"{ram_gb} GB"
    except (ValueError, OSError):
        return None
    return None


def _get_hypervisor() -> str | None:
    """Detect if the system is running under virtualization."""
    hyper_path = Path("/sys/hypervisor/type")
    if hyper_path.exists():
        val = _read_sysfs_file(str(hyper_path))
        if val:
            return val.capitalize()

    sys_vendor = _read_sysfs_file("/sys/class/dmi/id/sys_vendor")
    if sys_vendor:
        vendor_lower = sys_vendor.lower()
        if "qemu" in vendor_lower or "kvm" in vendor_lower:
            return "QEMU / KVM"
        if "vmware" in vendor_lower:
            return "VMware"
        if "innotek" in vendor_lower or "virtualbox" in vendor_lower:
            return "VirtualBox"

    return "Bare Metal"


def _get_boot_disk_model() -> str | None:
    """Identify the physical boot disk model."""
    disk_paths = [
        "/sys/block/nvme0n1/device/model",
        "/sys/block/sda/device/model",
        "/sys/block/vda/device/model",
        "/sys/block/mmcblk0/device/name",
    ]
    for p in disk_paths:
        val = _read_sysfs_file(p)
        if val:
            return val
    return None


def _get_primary_mac() -> str | None:
    """Fetch MAC address of the primary non-virtual network interface."""
    net_dir = Path("/sys/class/net")
    if not (net_dir.exists() and os.access(net_dir, os.R_OK)):
        return None

    try:
        for interface_path in net_dir.iterdir():
            if not interface_path.is_dir():
                continue

            iface_name = interface_path.name
            # Skip loopback and standard virtual/container bridges
            if iface_name == "lo" or iface_name.startswith(
                ("veth", "docker", "hassio", "br-", "tailscale", "wg", "tun", "tap")
            ):
                continue

            # Ensure interface is linked to physical hardware
            device_path = interface_path / "device"
            if not device_path.exists():
                continue

            mac_path = interface_path / "address"
            val = _read_sysfs_file(str(mac_path))
            if val and val != "00:00:00:00:00:00":
                return val.upper()
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

    # Read base sysfs files using executor
    for key, path in SYSFS_PATHS.items():
        val = await hass.async_add_executor_job(_read_sysfs_file, path)
        sensors.append(SystemHardwareSensor(entry, key, val))

    # CPU Model sensor
    cpu_val = await hass.async_add_executor_job(_get_cpu_model)
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_MODEL, cpu_val))

    # v1.1.0 Sensors
    cpu_cores = os.cpu_count()
    sensors.append(
        SystemHardwareSensor(
            entry, KEY_CPU_CORES, str(cpu_cores) if cpu_cores else None
        )
    )

    sensors.append(SystemHardwareSensor(entry, KEY_CPU_ARCH, platform.machine()))

    ram_val = await hass.async_add_executor_job(_get_total_ram)
    sensors.append(SystemHardwareSensor(entry, KEY_TOTAL_RAM, ram_val))

    hyp_val = await hass.async_add_executor_job(_get_hypervisor)
    sensors.append(SystemHardwareSensor(entry, KEY_HYPERVISOR, hyp_val))

    disk_val = await hass.async_add_executor_job(_get_boot_disk_model)
    sensors.append(SystemHardwareSensor(entry, KEY_BOOT_DISK, disk_val))

    mac_val = await hass.async_add_executor_job(_get_primary_mac)
    sensors.append(SystemHardwareSensor(entry, KEY_PRIMARY_MAC, mac_val))

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
