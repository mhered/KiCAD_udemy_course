"""
test_i2c.py — I2C bus scan.

Scans the I2C1 bus and reports detected devices.
Passes if the SHT31 (0x44) is found.
"""

import asyncio
from lib.utils import wait_ready, flash_result


async def test_i2c_scan(hw, cfg, state):
    """
    Scan I2C bus, report addresses, pass if SHT31 is present.
    Returns True on PASS, False on FAIL.
    """
    expected_addr = cfg["i2c"]["sht31_address"]  # 68 decimal = 0x44
    button = hw["button"]

    await wait_ready(hw, button)
    state["instructions"] = "Scanning I2C bus…"
    print("  Scanning I2C bus…")

    try:
        devices = hw["i2c"].scan()
    except Exception as e:
        print(f"  I2C scan error: {e}")
        state["instructions"] = f"I2C scan error: {e}"
        await flash_result(hw, False)
        return False

    if devices:
        addrs_str = ", ".join(f"0x{a:02X}" for a in devices)
        print(f"  Devices found: {addrs_str}")
        state["instructions"] = f"I2C devices: {addrs_str}"
    else:
        print("  No I2C devices found.")
        state["instructions"] = "I2C: no devices found"
        await flash_result(hw, False)
        return False

    if expected_addr in devices:
        print(f"  SHT31 detected at 0x{expected_addr:02X} ✓")
        await flash_result(hw, True)
        return True
    else:
        print(f"  SHT31 (0x{expected_addr:02X}) NOT found.")
        await flash_result(hw, False)
        return False
