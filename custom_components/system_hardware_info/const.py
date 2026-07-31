# custom_components/system_hardware_info/const.py
"""Constants for the System Hardware Info integration."""

from typing import Final

DOMAIN: Final[str] = "system_hardware_info"
MANUFACTURER: Final[str] = "ticstyle"
DEFAULT_NAME: Final[str] = "System Hardware Info"

# Sensor Keys
KEY_BOARD_NAME: Final[str] = "board_name"
KEY_BOARD_VENDOR: Final[str] = "board_vendor"
KEY_BIOS_VERSION: Final[str] = "bios_version"
KEY_SYS_VENDOR: Final[str] = "sys_vendor"
KEY_PRODUCT_NAME: Final[str] = "product_name"
KEY_CPU_MODEL: Final[str] = "cpu_model"

SYSFS_PATHS: Final[dict[str, str]] = {
    KEY_BOARD_NAME: "/sys/class/dmi/id/board_name",
    KEY_BOARD_VENDOR: "/sys/class/dmi/id/board_vendor",
    KEY_BIOS_VERSION: "/sys/class/dmi/id/bios_version",
    KEY_SYS_VENDOR: "/sys/class/dmi/id/sys_vendor",
    KEY_PRODUCT_NAME: "/sys/class/dmi/id/product_name",
}
