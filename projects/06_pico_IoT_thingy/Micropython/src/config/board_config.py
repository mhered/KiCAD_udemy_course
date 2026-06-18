"""
board_config.py — Board configuration for pico_IoT_thingy QC firmware.

Edit this file for board revisions.
WiFi credentials live in secrets.py (not tracked in git).
"""

CFG = {
    "timeouts": {
        "default":    30,
        "button":     15,
        "dip_switch": 60,
        "relay":      20,
        "rs485":      10,
        "spi":        10,
    },

    "pins": {
        # Output
        "relay":     11,
        # Input
        "button":    13,
        # RGB LED (PWM, common anode — active low)
        # NOTE: If Green is dead and Red/Blue appear swapped, LED is upside-down —
        # rotate 180° to fix. No code change needed for that fault.
        # NOTE: For BGRA-type RGB LED GPIO16=Red, GPIO18=Blue.
        "led_red":   16,
        "led_green": 17,
        "led_blue":  18,
        # DIP switches (active low, LSB=DIP1)
        "dip4":      19,
        "dip3":      20,
        "dip2":      21,
        "dip1":      22,
        # RS485 via THVD1406 (UART0, auto-direction)
        "rs485_tx":   0,
        "rs485_rx":   1,
        # SPI0
        "spi_sck":    2,
        "spi_mosi":   3,
        "spi_miso":   4,
        "spi_cs":     5,
        # I2C1
        "i2c_sda":    6,
        "i2c_scl":    7,
    },

    "i2c": {
        "frequency":     100_000,
        "sht31_address": 0x44,   # 68 decimal, assumes jumper JP1 open 
    },

    "rs485": {
        "baudrate":    9600,
        "test_string": "HELLO_RS485\r\n",
    },

    "spi": {
        "baudrate": 1_000_000,
    },
}
