# Prompt



You are an expert embedded firmware engineer specialized in MicroPython and Raspberry Pi Pico / RP2040 systems.

Your task is to implement a simple, robust manufacturing/QC firmware for a custom RP2040 board based on the Raspberry Pi Pico.

The purpose of the firmware is to quickly validate after manufacturing that:

- components are assembled correctly
- GPIO routing is correct
- connectors are operational
- buses are functional
- LEDs/buttons/switches work
- communication interfaces work

This is NOT intended to be exhaustive validation or production application firmware.

Keep the implementation:

- simple
- readable
- robust
- easy to maintain
- easy to adapt to future board revisions

Avoid overengineering.

# IMPORTANT ARCHITECTURE REQUIREMENTS

The firmware must support TWO simultaneous operator interfaces:

1. USB CDC serial console
2. Simple web page over WiFi

Use:

- USB CDC serial for logs and operator interaction
- UART0 exclusively for RS485 testing

Do NOT use UART0 for debugging.

# USB CDC SERIAL

All print() output should appear on the USB serial console automatically.

This console is the main debugging and manufacturing interface.

# WIFI + WEB INTERFACE

At startup:

- connect to WiFi using credentials from config file
- print assigned IP address
- start a VERY SIMPLE HTTP server

The web page should:

- auto-refresh every few seconds
- display current test step
- display instructions
- display PASS/FAIL status
- display final summary

Use plain HTML only.
Do NOT implement complex web frameworks.

If WiFi connection fails:

- continue operating normally over USB serial.

# PROJECT STRUCTURE

/main.py
/config/board_config.json
/tests/
/lib/

Keep modules lightweight and simple.

# CONFIGURATION FILE

All settings and timeouts must come from two python configuration files:

a secrets file that wont be tracked for wifi ssid and pwd 

a config file for the rest of the constants

Examples:

(secret)

```python
# suitable comments
WIFI_SSID = "YOUR_WIFI"
WIFI_PWD = "YOUR_PASSWORD"
```

(config)

```python
TIMEOUT_ DEFAULT = 30
TIMEOUT_ BUTTON = 15
TIMEOUT_ DIP_SWITCH = 60
TIMEOUT_ RELAY = 20
TIMEOUT_ RS485 = 10
TIMEOUT_ SPI = 10
```



# BOARD HARDWARE DESCRIPTION

------

## SWD CONNECTOR

The SWD connector exposes:

- SWCLK
- SWDIO
- GND

No firmware test required.
Assume SWD is validated during programming.

------

## RELAY

GPIO11 -> relay control

When GPIO11 is HIGH:

- relay activates
- yellow LED labelled OUT illuminates

Note:

- relay NO and NC silkscreen labels are incorrect
- firmware only needs to test relay activation

------

## USER BUTTON

GPIO12

------

## RESET BUTTON

Connected to RUN pin.

No firmware test required.

------

## RGB LED

GPIO16 -> Blue
GPIO17 -> Green
GPIO18 -> Red

Use PWM for brightness control and color mixing.

IMPORTANT:
PWM is supported even though these pins are not ADC pins.

------

## DIP SWITCH

GPIO19 -> DIP4
GPIO20 -> DIP3
GPIO21 -> DIP2
GPIO22 -> DIP1

Interpret DIP1 as LSB.

Compute MODBUS address from DIP state.

Example:
0001 -> address 1
0010 -> address 2
1111 -> address 15

Display detected MODBUS address during testing.

------

## RS485

THVD1406 transceiver.

UART mapping:
GPIO0 -> UART0_TX -> transceiver D
GPIO1 -> UART0_RX -> transceiver R

The THVD1406 uses AUTO-DIRECTION MODE.

SHDN and RE are tied HIGH in hardware.

This means:

- firmware does NOT need DE/RE control GPIOs
- simply using UART TX/RX is sufficient

Use UART0 exclusively for RS485 testing.

------

## RS485 TERMINATION JUMPER

J7 enables a 120 ohm resistor between A and B.

This is the RS485 termination resistor.

The firmware does not need to control it.

Assume:

- during QC testing J7 may be installed

------

## SPI CONNECTOR

GPIO2 -> SPI SCK
GPIO3 -> SPI MOSI/TX
GPIO4 -> SPI MISO/RX
GPIO5 -> SPI CSn

Also exposed:

- 3V3
- GND
- GPIO26/ADC0
- GPIO27/ADC1

------

## I2C

GPIO6 -> SDA
GPIO7 -> SCL

SHT31 sensor address:
0x44

QWIIC connector shares this I2C bus.

# IMPORTANT LIBRARY REQUIREMENT

Do NOT implement a custom SHT31 driver.

Instead:

- use an existing reliable MicroPython SHT31 library: https://github.com/kfricke/micropython-sht31
- clearly indicate where the library should be installed

# REQUIRED TEST SEQUENCE

Implement tests in the following order.

------

1. STARTUP

------

On startup:

- print firmware banner
- load JSON config
- validate config
- initialize peripherals
- connect WiFi
- start web server

Example:

Print assigned IP address if WiFi succeeds.

------

2. RGB LED TEST

------

Cycle:

- red
- green
- blue
- white
- off

Use PWM.

Ask operator to confirm visually using USER button.

------

3. USER BUTTON TEST

------

Ask operator to:

- press
- release

three times.

Use timeout protection.

------

4. DIP SWITCH TEST

------

Guide operator through:
0001
0010
0100
1000
1111
0000

Wait until expected pattern detected.

Display interpreted MODBUS address.

Use timeout protection.

------

5. I2C BUS SCAN

------

Scan I2C bus.

Display detected addresses.

Expected:

- SHT31 at 0x44

------

6. SHT31 TEST

------

Read temperature and humidity five times.

Validate:

- no exceptions
- reasonable values

Temperature:
0C to 50C

Humidity:
10% to 90%

Display measurements.

------

7. QWIIC CONNECTOR TEST

------

Ask operator to plug external I2C device.

Rescan bus.

Pass if a new address appears.

------

8. RELAY TEST

------

Toggle relay:
ON/OFF three times.

Ask operator to confirm:

- relay click
- yellow OUT LED illumination

Use USER button confirmation.

------

9. RS485 TEST

------

Implement SIMPLE UART echo test.

Assume:

- external RS485 echo dongle exists
  OR
- PC-based echo script exists

Procedure:

- send test string
- wait for echoed data
- compare response

Use UART0.

No DE/RE control required because THVD1406 auto-direction mode is enabled in hardware.

Display:

- transmitted bytes
- received bytes

------

10. SPI TEST

------

Implement SPI loopback test.

Assume:

- MOSI and MISO are externally connected using a jumper or test jig

Send bytes:
0x55
0xAA
0xDE
0xAD

Verify received bytes match.

------

11. FINAL SUMMARY

------

Display summary:

RGB LED ........ PASS
BUTTON ......... PASS
I2C ............ PASS
RS485 .......... FAIL

etc.

Then print:

BOARD RESULT: PASS

or:

BOARD RESULT: FAIL

# TIMEOUT REQUIREMENTS

Timeouts must be configurable via JSON.

If timeout occurs:

- mark test FAIL
- continue to next test

# CODING STYLE REQUIREMENTS

- Keep code simple and readable.
- Prefer functions over unnecessary classes.
- Avoid excessive abstraction.
- Use comments where useful.
- Handle exceptions gracefully.
- Avoid infinite blocking loops.
- Avoid hardcoded GPIO values outside configuration.

# WEB PAGE REQUIREMENTS

The web page should display:

- current test
- instructions
- PASS/FAIL results
- final summary

Plain HTML only.
No JavaScript frameworks.

# DELIVERABLES

Generate:

- main.py
- helper modules
- test modules
- minimal HTTP server
- example board_config.json
- instructions for installing SHT31 library
- instructions for RS485 echo setup
- instructions for SPI loopback setup

The generated code must run directly on Raspberry Pi Pico MicroPython.