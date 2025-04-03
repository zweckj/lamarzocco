> [!CAUTION]
> This integration does not support Gateway v5 (use the core integration instead) and is only intended for backwards compability.

# La Marzocco Home Assistant Integration (Gateway v3)

## Overview

This is an integration for recent La Marzocco espresso machines that use WiFi to connect to the cloud and can be controlled via the La Marzocco mobile app. This capability was rolled out in late 2019, and La Marzocco supposedly offers a retrofit kit to add it to earlier models. This repo started as fork for https://github.com/rccoleman/lamarzocco, but with the release of La Marzocco's Gateway V3 in 2023 became the new default.

Based on the investigation from Plonx on the Home Assistant forum [here](https://community.home-assistant.io/t/la-marzocco-gs-3-linea-mini-support/203581), this integration presents a comprehensive machine status through several entities and allows the user to change the machine configuration from Home Assistant.


### Bluetooth 
This integration can communicate to the machine through Bluetooth, in which case some of the commands (e.g. turning on/off) are not sent through the cloud. If your server doesn't have a bluetooth interface, or is not close enough to your machine ESPHome's [Bluetooth Proxies](https://esphome.github.io/bluetooth-proxies/) are a very good solution.

### WebSockets
This integration opens a WebSocket connection to your machine to stream information. In case you are encountering any issues, for example with the official app connecting, you can disable the WebSocket connections in the integration's settings.

###  Lovelace

A companion Lovelace card that uses this integration to retrieve data and control the machine can be found [here](https://github.com/rccoleman/lovelace-lamarzocco-config-card).

### Feedback

This integration currently only supports a single espresso machine. It's possible to support multiple machines, but I only have one and I suspect that'll be the case for most folks. If anyone has a fleet of espresso machines and is willing to provide data and feedback, We're happy to entertain adding support for more than one machine.

## Installation

### HACS

This integration is compatible with [HACS](https://hacs.xyz/), which means that you can easily download and manage updates for it. <br>
Click the button below to add it to your HACS installation <br>
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=zweckj&repository=lamarzocco&category=integration)

<!-- If you've installed [HACS](https://hacs.xyz), this integration is in the default list and you can simply search for "La Marzocco" and install it that way.

1. Launch the HACS panel from the left sidebar
2. Click "Integrations`
3. Search for "La Marzocco" and select it
4. Click "Install" on card that appears -->

or add the repo to HACS manually:

1. Launch the HACS panel from the left sidebar
2. Click "Integrations`
3. Click the three dots in the top right corner
4. Click "Add custom repository"
5. Add the link to this repo (`https://github.com/zweckj/lamarzocco`)
6. Click "Explore & Download Repositories"
7. Install "La Marzocco"
   
### Manual

If you don't have HACS installed or would prefer to install manually.

1. Create a `config/custom_comoponents` directory if it doesn't already exist
2. Clone this repo and move `lamarzocco` into `config/custom_components`. Your directory tree should look like `config/custom_components/lamarzocco/...files...`

#### Restart Home Assistant

## Configuration

Click the following button to set up this integration in Home Assistant.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=lamarzocco)

Alternatively, you may add the integration manually.

1. Navigate to Settings->Devices & Services
2. Hit the "+ Add Integration" button in the lower-right
3. Search for "La Marzocco" and select it
4. You'll be presented with a dialog box like this:

![Config Flow](https://github.com/zweckj/lamarzocco/blob/main/images/Config_Flow.png)

5. Fill in the info
6. Hit "Submit"

### Configured Integration

Once you configured the integration, you should see this in Configuration->Integrations:

<img width="261" alt="image" src="https://user-images.githubusercontent.com/860888/172060743-6438193e-7778-4c0e-8672-95fd9df2a856.png">

## Usage

In Dev->States, you should see several new entities, with your machine model dictating which ones:

  - `water_heater.<machine_name>_coffee`
  - `water_heater.<machine_name>_steam`
  - `sensor.<machine_name>_total_drinks`
  - `binary_sensor.<machine_name>_water_reservoir`
  - `switch.<machine_name>_main`
  - `switch.<machine_name>_auto_on_off`
  - `switch.<machine_name>_prebrew`
  - `switch.<machine_name>_preinfusion`
  - `button.<machine_name>_start_backflush`
  - `switch.<machine_name>_steam_boiler_enable`
  
Thw switches control their respective functions globally, i.e., enable/disable auto on/off for the whole machine, enable/disable prebrewing for all front-panel keys.

## Services

The `water_heater` and `switch` entities support the standard services for those domains, described [here](https://www.home-assistant.io/integrations/water_heater/) and [here](https://www.home-assistant.io/integrations/switch/), respectively.

The following domain-specific services are also available (model-dependent):

#### Service `lamarzocco.set_auto_on_off_enable`

Enable or disable auto on/off for a specific day of the week.

| Service data attribute | Optional | Description                                                                           |
| ---------------------- | -------- | ------------------------------------------------------------------------------------- |
| `day_of_week`          | no       | The day of the week to enable (sun, mon, tue, wed, thu, fri, sat)                     |
| `enable`               | no       | Boolean value indicating whether to enable or disable auto on/off, e.g. "on" or "off" |

#### Service `lamarzocco.set_auto_on_off_times`

Set the auto on and off times for each day of the week.

| Service data attribute | Optional | Description                                                       |
| ---------------------- | -------- | ----------------------------------------------------------------- |
| `day_of_week`          | no       | The day of the week to enable (sun, mon, tue, wed, thu, fri, sat) |
| `hour_on`              | no       | The hour to turn the machine on (0..23)                           |
| `minute_on`            | yes      | The minute to turn the machine on (0..59)                         |
| `hour_off`             | no       | The hour to turn the machine off (0..23)                          |
| `minute_off`           | yes      | The minute to turn the machine off (0..59)                        |

#### Service `lamarzocco.set_dose`

Sets the dose for a specific key.

| Service data attribute | Optional | Description                                             |
| ---------------------- | -------- | ------------------------------------------------------- |
| `key`                  | no       | The key to program (1-5)                                |
| `pulses`               | no       | The dose in pulses (roughly ~0.5ml per pulse), e.g. 120 |

#### Service `lamarzocco.set_dose_hot_water`

Sets the dose for hot water.

| Service data attribute | Optional | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `seconds`              | no       | The number of seconds to stream hot water, e.g. 8  |

#### Service `lamarzocco.set_prebrew_times`

Set the prebrewing "on" and "off" times for a specific key.

| Service data attribute | Optional | Description                                                         |
| ---------------------- | -------- | ------------------------------------------------------------------- |
| `key`                  | no       | The key to program (1-4)                                            |
| `seconds_on`           | no       | The time in seconds for the pump to run during prebrewing (0-5.9s)  |
| `seconds_off`          | no       | The time in seconds for the pump to stop during prebrewing (0-5.9s) |

#### Service `lamarzocco.set_preinfusion_time`

Set the preinfusion time for a specific key.

| Service data attribute | Optional | Description                                                         |
| ---------------------- | -------- | ------------------------------------------------------------------- |
| `key`                  | no       | The key to program (1-4)                                            |
| `seconds`              | no       | The time in seconds for preinfusion (0-24.9s)                        |

> **_NOTE:_** The machine won't allow more than one device to connect at once, so you may need to wait to allow the mobile app to connect while the integration is running. The integration only maintains the connection while it's sending or receiving information and polls every 30s, so you should still be able to use the mobile app.

If you have any questions or find any issues, either file them here or post to the thread on the Home Assistant forum [here](https://community.home-assistant.io/t/la-marzocco-gs-3-linea-mini-support/203581).
