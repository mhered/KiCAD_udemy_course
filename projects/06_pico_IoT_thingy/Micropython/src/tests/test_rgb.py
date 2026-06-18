"""
test_rgb.py — RGB LED test.

Cycles through RED, GREEN, BLUE, WHITE, then OFF.
Asks the operator to confirm visually using the USER button.
"""

import asyncio
from lib.hardware import set_rgb, rgb_off
from lib.utils import wait_button_press, wait_ready, flash_result

_COLORS = [
    ("RED",   255,   0,   0),
    ("GREEN",   0, 255,   0),
    ("BLUE",    0,   0, 255),
    ("WHITE", 255, 255, 255),
]


async def test_rgb_led(hw, cfg, state):
    """
    Show each color and wait for USER BUTTON confirmation before moving on.
    Returns True if all colors confirmed, False on any timeout.
    """
    timeout_ms = cfg["timeouts"]["button"] * 1000
    button = hw["button"]

    await wait_ready(hw, button)
    print(f"  Press USER BUTTON to confirm each color.  (timeout {cfg['timeouts']['button']} s each)")

    for name, r, g, b in _COLORS:
        set_rgb(hw, r, g, b)
        state["instructions"] = f"RGB LED: is it {name}? Press USER BUTTON to confirm."
        print(f"  [{name}] — press USER BUTTON to confirm…")

        if not await wait_button_press(button, timeout_ms):
            print(f"  TIMEOUT waiting for confirmation of {name}.")
            rgb_off(hw)
            await flash_result(hw, False)
            return False

        print(f"  {name} confirmed.")

    # OFF step
    rgb_off(hw)
    state["instructions"] = "RGB LED: is it OFF? Press USER BUTTON to confirm."
    print("  [OFF] — press USER BUTTON to confirm LED is off…")

    if not await wait_button_press(button, timeout_ms):
        print("  TIMEOUT waiting for confirmation of OFF.")
        await flash_result(hw, False)
        return False

    print("  OFF confirmed.")
    rgb_off(hw)
    await flash_result(hw, True)
    return True
