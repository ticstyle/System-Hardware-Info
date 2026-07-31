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

A modern Home Assistant custom integration that automatically reads hardware specifications from Linux DMI/sysfs and exposes detailed system, motherboard, BIOS, and CPU information directly inside Home Assistant.

To add this integration, please add the custom repository `https://github.com/ticstyle/System-Hardware-Info` to HACS in your Home Assistant setup.

## 🌐 Supported Languages / Språk
The integration natively defaults to English for backend operations but includes full frontend translations for Swedish. Thanks to native State Translations, sensor names will display localized text (e.g., *Moderkort*, *BIOS-version*, *CPU-modell*) seamlessly in your UI while maintaining clean system attributes.

## ✨ Features
* **Device-Centric Architecture:** Automatically creates a single **System Hardware Info** Device container grouping all hardware specs cleanly together (`manufacturer="ticstyle"`, `model="System Hardware Info"`).
* **🖥️ Deep Hardware Discovery:** Safe, native parsing of Linux system interfaces (`/sys/class/dmi/id/*` and `/proc/cpuinfo`) to pull physical host specs.
* **🏷️ Normalized Entity IDs:** All registered entities strictly start with the `sensor.system_hardware_info_` prefix for uniform entity tracking and clean automations.
* **⚙️ UI Reconfiguration & Self-Cleaning:** Supports native UI reconfiguration steps and automatically purges orphaned entities if hardware parameters change.
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
| `sensor.system_hardware_info_cpu_model` | CPU Model | `Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz` | Model string parsed directly from `/proc/cpuinfo`. |
| `sensor.system_hardware_info_board_name` | Motherboard | `PRIME Z370-A` | Motherboard model name from sysfs. |
| `sensor.system_hardware_info_board_vendor` | Motherboard Vendor | `ASUSTeK COMPUTER INC.` | Motherboard manufacturer name from sysfs. |
| `sensor.system_hardware_info_bios_version` | BIOS Version | `2401` | Active system BIOS/UEFI version string. |
| `sensor.system_hardware_info_sys_vendor` | System Vendor | `System manufacturer` | System enclosure / host vendor identifier. |
| `sensor.system_hardware_info_product_name` | Product Name | `System Product Name` | Hardware product model identifier. |

---

## 💡 Lovelace Dashboard Examples

### Example 1: Hardware Summary Markdown Card
Display host specifications cleanly in your Home Assistant dashboard:

```yaml
type: markdown
title: "🖥️ Host System Hardware"
content: >
  **CPU:** {{ states('sensor.system_hardware_info_cpu_model') }}
  
  **Motherboard:** {{ states('sensor.system_hardware_info_board_vendor') }} {{ states('sensor.system_hardware_info_board_name') }}
  
  **BIOS Version:** {{ states('sensor.system_hardware_info_bios_version') }}
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
  - entity: sensor.system_hardware_info_board_name
    name: "Motherboard"
    icon: mdi:developer-board
  - entity: sensor.system_hardware_info_board_vendor
    name: "Manufacturer"
    icon: mdi:factory
  - entity: sensor.system_hardware_info_bios_version
    name: "BIOS Revision"
    icon: mdi:memory
```
