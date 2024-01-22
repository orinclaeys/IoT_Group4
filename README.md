# Mars Rover IoT Project

## Overview
This repository contains the code and configuration for our IoT 'Mars Rover' project, developed as part of a master's thesis in IoT. The project includes a rover controlled via a base station, designed for autonomous exploration and data collection with a focus on low power consumption.

## Repository Structure
- IoT_Group4_LineBotCode.zip: This archive contains the complete code for the Linebot, integral to the rover's control system.

- IoT_Group4_STMCode.zip: This file includes the code for the STM microcontroller, a crucial component of the rover's hardware.

- Peripheral.ino: Script for the BLE (Bluetooth Low Energy) module setup in peripheral mode, enabling rover communication.

- PinConfig - V2.txt: A detailed pin configuration file, outlining the hardware connections and setup for the rover.

- centr.ino: Script for the BLE module in central mode, crucial for managing communication between different components of the rover.

- gasbusters_pull.zip: Contains the DASH7 end node code, essential for long-range communication with the base station.

- gasbusters_query_nodes.py: Python script for the DASH7 gateway, facilitating data query and transmission.

- influxdb_gas.zip: Archive containing resources and scripts for setting up and managing the project's InfluxDB, used for storing and handling the data collected by the rover.

## Hardware
- Linebot with XMEGA processor
- STM32 microcontroller
- BLE modules
- DASH7 end node
- Power management

## Software
- STM32 Cude IDE
- Microchip studio
- Arduino IDE
- Grafana
- InfluxDB

## Usage
- Upload the corresponding code to each module: Linebot, STM32, BLE, and DASH7.
- Ensure proper hardware connections as outlined in the `PinConfig/` directory.

## Contributors
Ahmad Alkhiami, Orin Claeys, Dante De Meyer, Barbora Havránková​


