"""
test_qwiic.py — QWIIC connector I2C test.

Asks the operator to plug an external I2C device into the QWIIC
connector and press USER BUTTON.  Scans the I2C bus once and passes
if at least one address beyond the on-board SHT31 is found.

The on-board SHT31 address (0x44 or 0x45, set by JP1) is read from
cfg["i2c"]["sht31_address"].
"""

import asyncio
from lib.utils import wait_button_press, wait_ready, flash_result


async def test_qwiic(hw, cfg, state):
    """
    Scan I2C bus after operator plugs in a QWIIC device.
    Passes if at least one address beyond the on-board SHT31 is found.
    Returns True on PASS, False on FAIL/timeout.
    """
    timeout_ms = cfg["timeouts"]["default"] * 1000
    button     = hw["button"]
    sht31_addr = cfg["i2c"]["sht31_address"]

    await wait_ready(hw, button)
    state["instructions"] = "Plug a QWIIC device, then press USER BUTTON to scan."
    print(f"  On-board SHT31 expected at 0x{sht31_addr:02X}.")
    print("  Plug an external I2C device into the QWIIC connector.")
    print("  Press USER BUTTON when ready to scan.")

    if not await wait_button_press(button, timeout_ms):
        print("  TIMEOUT — no button press received.")
        state["instructions"] = "QWIIC: timeout"
        await flash_result(hw, False)
        return False

    # Scan
    try:
        found = set(hw["i2c"].scan())
    except Exception as e:
        print(f"  I2C scan error: {e}")
        await flash_result(hw, False)
        return False

    found_str = ", ".join(f"0x{a:02X}" for a in sorted(found)) or "none"
    print(f"  I2C devices found: {found_str}")

    extra = found - {sht31_addr}

    if extra:
        extra_str = ", ".join(f"0x{a:02X}" for a in sorted(extra))
        print(f"  QWIIC device(s) detected: {extra_str} ✓")
        state["instructions"] = f"QWIIC: device(s) at {extra_str}"
        await flash_result(hw, True)
        return True
    else:
        print("  No QWIIC device detected beyond on-board SHT31.")
        state["instructions"] = "QWIIC: no QWIIC device detected"
        await flash_result(hw, False)
        return False
