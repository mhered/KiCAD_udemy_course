"""
hardware.py — Hardware initialisation for pico_IoT_thingy QC firmware.

Centralises every GPIO/peripheral definition so board revisions only
require editing config/board_config.py (and this file if a new peripheral
category is added).
"""

import machine


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config():
    """Import and return the CFG dict from config/board_config.py."""
    from config.board_config import CFG
    return CFG


# ---------------------------------------------------------------------------
# Peripheral initialisation
# ---------------------------------------------------------------------------

def init_hardware(cfg):
    """
    Initialise all board peripherals from config.
    Returns a dict of hardware handles keyed by name.
    """
    p = cfg["pins"]
    hw = {}

    # --- Relay (active high, starts OFF) -----------------------------------
    hw["relay"] = machine.Pin(p["relay"], machine.Pin.OUT, value=0)

    # --- User button (active low, internal pull-up) -------------------------
    hw["button"] = machine.Pin(p["button"], machine.Pin.IN, machine.Pin.PULL_UP)

    # --- RGB LED via PWM (active high, 0 duty = OFF) ------------------------
    # GPIO16/17/18 support PWM even though they are not ADC pins.
    hw["led_red"]   = machine.PWM(machine.Pin(p["led_red"]))
    hw["led_green"] = machine.PWM(machine.Pin(p["led_green"]))
    hw["led_blue"]  = machine.PWM(machine.Pin(p["led_blue"]))
    for ch in ("led_red", "led_green", "led_blue"):
        hw[ch].freq(1000)
        hw[ch].duty_u16(65535)  # common anode: 65535 = OFF

    # --- DIP switches (active low, internal pull-up) -----------------------
    # Switch ON (closed) → GPIO reads 0 → logical bit = 1
    hw["dip1"] = machine.Pin(p["dip1"], machine.Pin.IN, machine.Pin.PULL_UP)
    hw["dip2"] = machine.Pin(p["dip2"], machine.Pin.IN, machine.Pin.PULL_UP)
    hw["dip3"] = machine.Pin(p["dip3"], machine.Pin.IN, machine.Pin.PULL_UP)
    hw["dip4"] = machine.Pin(p["dip4"], machine.Pin.IN, machine.Pin.PULL_UP)

    # --- I2C1 on GPIO6 (SDA) / GPIO7 (SCL) ---------------------------------
    i2c_cfg = cfg["i2c"]
    hw["i2c"] = machine.I2C(
        1,
        sda=machine.Pin(p["i2c_sda"]),
        scl=machine.Pin(p["i2c_scl"]),
        freq=i2c_cfg["frequency"],
    )

    # --- UART0 for RS485 (GPIO0=TX, GPIO1=RX) --------------------------------
    # THVD1406 is in auto-direction mode; no DE/RE control needed.
    rs_cfg = cfg["rs485"]
    hw["uart"] = machine.UART(
        0,
        baudrate=rs_cfg["baudrate"],
        tx=machine.Pin(p["rs485_tx"]),
        rx=machine.Pin(p["rs485_rx"]),
    )

    # --- SPI0 on GPIO2(SCK)/3(MOSI)/4(MISO)/5(CS) --------------------------
    spi_cfg = cfg["spi"]
    hw["spi"] = machine.SPI(
        0,
        baudrate=spi_cfg["baudrate"],
        sck=machine.Pin(p["spi_sck"]),
        mosi=machine.Pin(p["spi_mosi"]),
        miso=machine.Pin(p["spi_miso"]),
    )
    hw["spi_cs"] = machine.Pin(p["spi_cs"], machine.Pin.OUT, value=1)

    return hw


# ---------------------------------------------------------------------------
# RGB LED helpers
# ---------------------------------------------------------------------------

def set_rgb(hw, r, g, b):
    """Set RGB LED brightness. r, g, b are 0–255.
    LED is common anode: duty=0 → ON, duty=65535 → OFF.
    """
    hw["led_red"].duty_u16((255 - r) * 257)
    hw["led_green"].duty_u16((255 - g) * 257)
    hw["led_blue"].duty_u16((255 - b) * 257)


def rgb_off(hw):
    """Turn all RGB LED channels off."""
    set_rgb(hw, 0, 0, 0)


# ---------------------------------------------------------------------------
# DIP switch helper
# ---------------------------------------------------------------------------

def read_dip(hw):
    """
    Read DIP switch state.

    Switches are active-low (ON=0 on GPIO → logical 1).
    DIP1 is LSB, DIP4 is MSB.

    Returns:
        address (int):  MODBUS address 0–15
        bits (str):     4-character binary string "DIP4 DIP3 DIP2 DIP1"
    """
    b1 = 1 - hw["dip1"].value()
    b2 = 1 - hw["dip2"].value()
    b3 = 1 - hw["dip3"].value()
    b4 = 1 - hw["dip4"].value()
    address = (b4 << 3) | (b3 << 2) | (b2 << 1) | b1
    bits = f"{b4}{b3}{b2}{b1}"
    return address, bits
