# System Hardware Info

![Latest Release](https://img.shields.io/github/v/release/ticstyle/System-Hardware-Info?color=blue&label=Release)
![Last Updated](https://img.shields.io/github/last-commit/ticstyle/System-Hardware-Info?path=hacs.json&label=Maintained)
![Issues](https://img.shields.io/github/issues/ticstyle/System-Hardware-Info?color=orange&label=Issues)
![Custom Integration](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-blue?logo=home-assistant)
![Home Assistant Required Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/ticstyle/System-Hardware-Info/main/hacs.json&query=%24.homeassistant&suffix=%2B&label=Home%20Assistant&logo=homeassistant)

![License](https://img.shields.io/github/license/ticstyle/System-Hardware-Info?label=License)
[![Hassfest](https://img.shields.io/github/actions/workflow/status/ticstyle/System-Hardware-Info/pipeline.yml?branch=main&job=hassfest&label=Hassfest)](https://github.com/ticstyle/System-Hardware-Info/actions/workflows/pipeline.yml)
[![HACS Validation](https://img.shields.io/github/actions/workflow/status/ticstyle/System-Hardware-Info/pipeline.yml?branch=main&job=hacs&label=HACS)](https://github.com/ticstyle/System-Hardware-Info/actions/workflows/pipeline.yml)
[![Ruff / Format](https://img.shields.io/github/actions/workflow/status/ticstyle/System-Hardware-Info/pipeline.yml?branch=main&job=sync_and_format&label=Ruff%20%2F%20Format)](https://github.com/ticstyle/System-Hardware-Info/actions/workflows/pipeline.yml)
[![Mypy](https://img.shields.io/github/actions/workflow/status/ticstyle/System-Hardware-Info/pipeline.yml?branch=main&job=mypy&label=Mypy)](https://github.com/ticstyle/System-Hardware-Info/actions/workflows/pipeline.yml)
![Installs](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=Known%20installs&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.System-Hardware-Info.total)

A modern Home Assistant custom integration that automatically reads hardware specifications from Linux DMI/sysfs and exposes detailed system, motherboard, BIOS, physical storage, network, and CPU information directly inside Home Assistant.

To add this integration, please add the custom repository `https://github.com/ticstyle/System-Hardware-Info` to HACS in your Home Assistant setup.

## ✨ Features
* **🖥️ Deep Hardware Discovery:** Safe, native parsing of Linux system interfaces (`/sys/class/dmi/id/*`, `/proc/cpuinfo`, and sysfs network/block devices) to pull physical host specs.
* **🔒 Privacy & Executor Safe:** Offloads file reading to background executor threads to ensure zero blocking calls in the Home Assistant event loop.
* **🔍 Built-in Diagnostics:** Complete support for Home Assistant Diagnostics (`diagnostics.py`) to quickly copy hardware summaries with safe data isolation.
* **⚡ Zero-Impact Polling:** Reads static host specifications on initial startup without wasting background CPU cycles.

## 🚀 Installation

[![](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ticstyle&repository=System-Hardware-Info&category=Integration)

Via [HACS](https://hacs.xyz/) or manually copy the `system_hardware_info` folder from the [latest release](https://github.com/ticstyle/System-Hardware-Info/releases/latest) to the `custom_components` folder inside your Home Assistant configuration directory.

## ⚙️ Configuration

[![](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=system_hardware_info)

Add the integration via the Home Assistant User Interface. Go to **Settings -> Devices & Services -> Add Integration** and search for **System Hardware Info**. 

Setup is fully automatic with a zero-configuration flow. Once added, the device and all associated hardware entities are populated immediately.

## 📊 Available Entities
Once configured, the integration automatically registers a device named **System Hardware Info** containing the following entities:

| Entity ID | Name in UI | State Example | Description |
| :--- | :--- | :--- | :--- |
| `sensor.system_hardware_info_cpu_model` | CPU | `Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz` | Model string parsed directly from `/proc/cpuinfo`. |
| `sensor.system_hardware_info_cpu_vendor` | CPU Vendor | `GenuineIntel` | CPU vendor string from `/proc/cpuinfo`. |
| `sensor.system_hardware_info_cpu_cores` | CPU Cores | `6` | Total logical processor core count. |
| `sensor.system_hardware_info_cpu_arch` | CPU Architecture | `x86_64` | Host system architecture (`x86_64`, `aarch64`, etc.). |
| `sensor.system_hardware_info_cpu_max_freq` | CPU Max Frequency | `4.00 GHz` | Rated factory maximum processor clock speed. |
| `sensor.system_hardware_info_hardware_virt` | Hardware Virtualization | `Enabled` | Checks for VT-x / AMD-V flag support (`vmx`/`svm`). |
| `sensor.system_hardware_info_total_ram` | Total Installed RAM | `16.0 GB` | Total physical memory capacity installed on host. |
| `sensor.system_hardware_info_board_name` | Motherboard | `PRIME Z370-A` | Motherboard model name from sysfs. |
| `sensor.system_hardware_info_board_vendor` | Motherboard Vendor | `ASUSTeK COMPUTER INC.` | Motherboard manufacturer name from sysfs. |
| `sensor.system_hardware_info_board_version` | Motherboard Revision | `Rev 1.02` | Revision or version identifier of motherboard. |
| `sensor.system_hardware_info_bios_version` | Motherboard BIOS version | `2401` | Active system BIOS/UEFI version string. |
| `sensor.system_hardware_info_bios_date` | BIOS Date | `2024-04-18` | BIOS release date normalized strictly to `YYYY-MM-DD`. |
| `sensor.system_hardware_info_hypervisor` | Virtualization Host | `Bare Metal` or `QEMU / KVM` | Detects hypervisor environment (Proxmox, VMware, Bare Metal, etc.). |
| `sensor.system_hardware_info_boot_disk_model` | Boot Disk Model | `Samsung SSD 980 500GB` | Physical primary boot drive model name. |
| `sensor.system_hardware_info_primary_mac` | Primary MAC Address | `AA:BB:CC:DD:EE:FF` | Hardware MAC address of active primary network adapter. |
| `sensor.system_hardware_info_sys_vendor` | System Vendor | `System manufacturer` | System enclosure / host vendor identifier. |
| `sensor.system_hardware_info_product_name` | Product Name | `System Product Name` | Hardware product model identifier. |
| `sensor.system_hardware_info_product_family` | Product Family | `ThinkCentre` | Hardware product family or line string from DMI. |
| `sensor.system_hardware_info_kernel_version` | Kernel Version | `6.6.73-haos` | Active Linux kernel version running on the host. |

---

## 💡 Lovelace Dashboard Examples

### Example 1: Hardware Summary Markdown Card
Display host specifications cleanly in your Home Assistant dashboard:

```yaml
type: markdown
title: "🖥️ Host Hardware Summary"
content: >
  **CPU:** {{ states('sensor.system_hardware_info_cpu_model') }} ({{ states('sensor.system_hardware_info_cpu_cores') }} Cores, {{ states('sensor.system_hardware_info_cpu_arch') }})
  
  **RAM:** {{ states('sensor.system_hardware_info_total_ram') }}
  
  **Motherboard:** {{ states('sensor.system_hardware_info_board_vendor') }} {{ states('sensor.system_hardware_info_board_name') }}
  
  **BIOS:** {{ states('sensor.system_hardware_info_bios_version') }} (Dated {{ states('sensor.system_hardware_info_bios_date') }})
  
  **Virtualization:** {{ states('sensor.system_hardware_info_hypervisor') }}
```

### Example 2: Complete Hardware Spec Entities Card
A sleek list card grouping all discovered specs under the System Hardware Info device:

```yaml
type: entities
title: "System Hardware Specifications"
icon: mdi:cpu-64-bit
entities:
  - entity: sensor.system_hardware_info_cpu_model
    name: "Processor"
    icon: mdi:chip
  - entity: sensor.system_hardware_info_total_ram
    name: "Installed RAM"
    icon: mdi:memory
  - entity: sensor.system_hardware_info_board_name
    name: "Motherboard"
    icon: mdi:developer-board
  - entity: sensor.system_hardware_info_bios_version
    name: "BIOS Revision"
    icon: mdi:chip
  - entity: sensor.system_hardware_info_hypervisor
    name: "Environment"
    icon: mdi:server
  - entity: sensor.system_hardware_info_boot_disk_model
    name: "Boot Storage"
    icon: mdi:harddisk
  - entity: sensor.system_hardware_info_primary_mac
    name: "Primary MAC"
    icon: mdi:ethernet
```
