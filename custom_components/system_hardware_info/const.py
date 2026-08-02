# custom_components/system_hardware_info/const.py
"""Constants for the System Hardware Info integration."""

from typing import Final

DOMAIN: Final[str] = "system_hardware_info"
MANUFACTURER: Final[str] = "ticstyle"
DEFAULT_NAME: Final[str] = "System Hardware Info"

# v1.0.0 Keys
KEY_BOARD_NAME: Final[str] = "board_name"
KEY_BOARD_VENDOR: Final[str] = "board_vendor"
KEY_BIOS_VERSION: Final[str] = "bios_version"
KEY_SYS_VENDOR: Final[str] = "sys_vendor"
KEY_PRODUCT_NAME: Final[str] = "product_name"
KEY_CPU_MODEL: Final[str] = "cpu_model"

# v1.1.0 Keys
KEY_CPU_CORES: Final[str] = "cpu_cores"
KEY_CPU_ARCH: Final[str] = "cpu_arch"
KEY_TOTAL_RAM: Final[str] = "total_ram"
KEY_HYPERVISOR: Final[str] = "hypervisor"
KEY_BOOT_DISK: Final[str] = "boot_disk_model"
KEY_PRIMARY_MAC: Final[str] = "primary_mac"

# v1.2.0 Keys
KEY_BIOS_DATE: Final[str] = "bios_date"
KEY_BOARD_VERSION: Final[str] = "board_version"
KEY_CPU_VENDOR: Final[str] = "cpu_vendor"
KEY_CPU_MAX_FREQ: Final[str] = "cpu_max_freq"
KEY_HARDWARE_VIRT: Final[str] = "hardware_virt"
KEY_PRODUCT_FAMILY: Final[str] = "product_family"
KEY_KERNEL_VERSION: Final[str] = "kernel_version"
KEY_USABLE_RAM: Final[str] = "usable_ram"

# v1.3.0 Keys
KEY_PCI_DEVICES_COUNT: Final[str] = "pci_devices_count"
KEY_GPU_MODEL: Final[str] = "gpu_model"
KEY_SYSTEM_CHASSIS: Final[str] = "system_chassis"
KEY_MOTHERBOARD_SERIAL: Final[str] = "motherboard_serial"
KEY_DISK_BUS_TYPE: Final[str] = "disk_bus_type"
KEY_BOOT_MODE: Final[str] = "boot_mode"
KEY_CPU_CACHE_L3: Final[str] = "cpu_cache_l3"

SYSFS_PATHS: Final[dict[str, str]] = {
    KEY_BOARD_NAME: "/sys/class/dmi/id/board_name",
    KEY_BOARD_VENDOR: "/sys/class/dmi/id/board_vendor",
    KEY_BIOS_VERSION: "/sys/class/dmi/id/bios_version",
    KEY_SYS_VENDOR: "/sys/class/dmi/id/sys_vendor",
    KEY_PRODUCT_NAME: "/sys/class/dmi/id/product_name",
    KEY_BOARD_VERSION: "/sys/class/dmi/id/board_version",
    KEY_PRODUCT_FAMILY: "/sys/class/dmi/id/product_family",
    KEY_MOTHERBOARD_SERIAL: "/sys/class/dmi/id/board_serial",
}
