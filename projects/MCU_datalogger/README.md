# README.md

A simple **microcontroller-based datalogger** designed to practice PCB design in KiCAD while introducing the fundamentals of embedded data acquisition. The board reads sensor data through the MCU and stores it in EEPROM, making it possible to log measurements over time.

The design covers the key building blocks of a typical datalogger system:

- **MCU (microcontroller)** – handles sensor interfacing, data collection, and storage management.
- **Sensors / Inputs** – generic sensor connections to capture physical measurements.
- **EEPROM** – nonvolatile memory to store logged data.
- **Power supply** – provides stable operation from external power or batteries.
- **Programming / Debug headers** – for uploading firmware and retrieving logged data (??)
