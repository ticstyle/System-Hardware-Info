# custom_components/system_hardware_info/sensor.py
"""Sensor platform for System Hardware Info."""

from __future__ import annotations

from datetime import UTC, datetime
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
    KEY_BIOS_DATE,
    KEY_BIOS_VERSION,
    KEY_BOOT_DISK,
    KEY_CPU_ARCH,
    KEY_CPU_CORES,
    KEY_CPU_MAX_FREQ,
    KEY_CPU_MODEL,
    KEY_CPU_VENDOR,
    KEY_HARDWARE_VIRT,
    KEY_HYPERVISOR,
    KEY_KERNEL_VERSION,
    KEY_PRIMARY_MAC,
    KEY_PRODUCT_NAME,
    KEY_TOTAL_RAM,
    KEY_USABLE_RAM,
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


def _get_bios_date() -> str | None:
    """Read BIOS release date and format strictly as YYYY-MM-DD."""
    raw_date = _read_sysfs_file("/sys/class/dmi/id/bios_date")
    if not raw_date:
        return None

    # Common SMBIOS formats: MM/DD/YYYY, MM/DD/YY, YYYY-MM-DD
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(raw_date, fmt).replace(tzinfo=UTC)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return raw_date


def _get_cpu_info() -> tuple[str | None, str | None, str | None]:
    """Extract model name, vendor ID, and virtualization capability from /proc/cpuinfo."""
    cpu_path = Path("/proc/cpuinfo")
    model: str | None = None
    vendor: str | None = None
    virt_capable: str | None = None

    if cpu_path.exists() and os.access(cpu_path, os.R_OK):
        try:
            lines = cpu_path.read_text(encoding="utf-8").splitlines()
            for line in lines:
                if "model name" in line and not model:
                    model = line.split(":", 1)[1].strip()
                elif "vendor_id" in line and not vendor:
                    vendor = line.split(":", 1)[1].strip()
                elif "flags" in line or "Features" in line:
                    flags = line.split(":", 1)[1].strip().split()
                    if "vmx" in flags or "svm" in flags:
                        virt_capable = "Enabled"
                    elif virt_capable is None:
                        virt_capable = "Disabled / Unsupported"
        except OSError:
            pass

    return model, vendor, virt_capable


def _get_cpu_max_freq() -> str | None:
    """Read factory maximum CPU clock frequency."""
    freq_path = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
    val = _read_sysfs_file(freq_path)
    if val and val.isdigit():
        khz = int(val)
        if khz >= 1000000:
            return f"{round(khz / 1000000, 2)} GHz"
        return f"{round(khz / 1000, 0):.0f} MHz"
    return None


def _get_total_ram() -> str | None:
    """Calculate installed physical RAM rounded to the nearest standard capacity."""
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        if pages > 0 and page_size > 0:
            raw_gb = (pages * page_size) / (1024**3)
            # Standard physical RAM module capacity sizes in GB
            standard_capacities = [1, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256]
            matched = min(standard_capacities, key=lambda x: abs(x - raw_gb))
            return f"{matched} GB"
    except (ValueError, OSError):
        return None
    return None


def _get_usable_ram() -> str | None:
    """Calculate usable kernel memory pages in GB."""
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        if pages > 0 and page_size > 0:
            usable_gb = round((pages * page_size) / (1024**3), 2)
            return f"{usable_gb} GB"
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
            if iface_name == "lo" or iface_name.startswith(
                ("veth", "docker", "hassio", "br-", "tailscale", "wg", "tun", "tap")
            ):
                continue

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

    # CPU info parsing
    cpu_model, cpu_vendor, virt_capable = await hass.async_add_executor_job(
        _get_cpu_info
    )
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_MODEL, cpu_model))
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_VENDOR, cpu_vendor))
    sensors.append(SystemHardwareSensor(entry, KEY_HARDWARE_VIRT, virt_capable))

    # BIOS Date formatted YYYY-MM-DD
    bios_date = await hass.async_add_executor_job(_get_bios_date)
    sensors.append(SystemHardwareSensor(entry, KEY_BIOS_DATE, bios_date))

    # CPU Max Freq
    max_freq = await hass.async_add_executor_job(_get_cpu_max_freq)
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_MAX_FREQ, max_freq))

    # Kernel version
    sensors.append(
        SystemHardwareSensor(entry, KEY_KERNEL_VERSION, platform.release())
    )

    # Core count & Architecture
    cpu_cores = os.cpu_count()
    sensors.append(
        SystemHardwareSensor(
            entry, KEY_CPU_CORES, str(cpu_cores) if cpu_cores else None
        )
    )
    sensors.append(SystemHardwareSensor(entry, KEY_CPU_ARCH, platform.machine()))

    # Memory sensors
    ram_val = await hass.async_add_executor_job(_get_total_ram)
    sensors.append(SystemHardwareSensor(entry, KEY_TOTAL_RAM, ram_val))

    usable_val = await hass.async_add_executor_job(_get_usable_ram)
    sensors.append(SystemHardwareSensor(entry, KEY_USABLE_RAM, usable_val))

    # Hypervisor, disk, MAC
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
        
