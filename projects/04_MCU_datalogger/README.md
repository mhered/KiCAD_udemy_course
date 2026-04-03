# README.md

A simple **microcontroller-based datalogger** designed to practice PCB design in KiCAD while introducing the fundamentals of embedded data acquisition. The board reads sensor data through the MCU and stores it in EEPROM, making it possible to log measurements over time.

The design covers the key building blocks of a typical datalogger system:

- **MCU (microcontroller)** – handles sensor interfacing, data collection, and storage management.
- **Sensors / Inputs** – generic sensor connections to capture physical measurements.
- **EEPROM** – nonvolatile memory to store logged data.
- **Power supply** – provides stable operation from external power or batteries.
- **Programming / Debug headers** – for uploading firmware and retrieving logged data (??)

DS1337S

ATMEGA328P-AU from SNAPEDA

## v1.0

![](./assets/MCU_datalogger_PCB_v1.0.png)

## v1.1

Adjust edges and silkscreen, add Vcc fill zone

![](./assets/MCU_datalogger_layout_v1.1.png)

![](./assets/MCU_datalogger_PCB_v1.1.png)

## Bootloading and firmware uploading the ATMEGA328

- Arduino to atmega328 [Arduino Uno to ATmega328 - Shrinking your Arduino ProjectsYouTube · DroneBot Workshop29 Dec 2018](https://www.youtube.com/watch?v=Sww1mek5rHU)
- Shrinking arduino projects atmega328 https://youtu.be/aex1HFhJG_g?si=vZYHLi1vfadTmJW0

- http://www.kerrywong.com/2010/09/25/i2c-data-logger-using-atmega328p-and-ds3232/

## v1.3

ChatGPT disagrees with the choice of an electrolytic 100nF capacitor in parallel with the battery it says it is too slow. and recommends instead a ceramic 100nF close to the MCU pins to act as filter for spikes. Optionally can add a 10-100uF bulk cap (e.g. electrolytic) to stabilize)

I cant find anything in the datasheet

Looks like EEPROM address is hardcoded 111 and 101, check datasheet!

