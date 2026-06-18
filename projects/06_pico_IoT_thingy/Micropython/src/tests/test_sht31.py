"""
test_sht31.py — SHT31 temperature/humidity sensor test.

Reads temperature and humidity five times and validates that each
reading is within a reasonable range for an indoor environment.

Requires the sht31 MicroPython library to be installed on the Pico.
See README.md for installation instructions.
"""

import asyncio
from lib.utils import wait_ready, flash_result

_READINGS = 5
_TEMP_MIN =  0.0   # °C
_TEMP_MAX = 50.0   # °C
_HUM_MIN  = 10.0   # %RH
_HUM_MAX  = 90.0   # %RH


async def test_sht31(hw, cfg, state):
    """
    Take five SHT31 readings and validate range.
    Returns True if all readings are valid, False otherwise.
    """
    state["instructions"] = "Reading SHT31 sensor…"
    button = hw["button"]

    await wait_ready(hw, button)
    # Import here so a missing library gives a clear error message
    try:
        import sht31
    except ImportError:
        print("  ERROR: sht31 library not found.")
        print("  Download sht31.py from https://github.com/kfricke/micropython-sht31")
        print("  and copy it to the Pico root:  mpremote cp sht31.py :sht31.py")
        state["instructions"] = "SHT31: library not installed (see README)"
        await flash_result(hw, False)
        return False

    sht31_addr = cfg["i2c"]["sht31_address"]

    try:
        sensor = sht31.SHT31(hw["i2c"], addr=sht31_addr)
    except Exception as e:
        print(f"  SHT31 init error: {e}")
        await flash_result(hw, False)
        return False

    passed = True
    for i in range(1, _READINGS + 1):
        try:
            temp, hum = sensor.get_temp_humi()
        except Exception as e:
            print(f"  Reading {i}: ERROR — {e}")
            passed = False
            await asyncio.sleep_ms(500)
            continue

        ok = (_TEMP_MIN <= temp <= _TEMP_MAX) and (_HUM_MIN <= hum <= _HUM_MAX)
        flag = "OK" if ok else "OUT OF RANGE"
        print(f"  Reading {i}: {temp:.1f} °C  {hum:.1f} %RH  [{flag}]")
        state["instructions"] = f"SHT31 #{i}: {temp:.1f}°C  {hum:.1f}%RH  {flag}"

        if not ok:
            passed = False

        await asyncio.sleep_ms(500)

    if passed:
        print("  All SHT31 readings valid.")
    else:
        print("  One or more SHT31 readings were invalid or out of range.")

    await flash_result(hw, passed)
    return passed
