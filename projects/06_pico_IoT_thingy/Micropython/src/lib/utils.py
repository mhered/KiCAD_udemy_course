"""
utils.py — Async helper utilities shared by all test modules.
"""

import time
import asyncio


# ---------------------------------------------------------------------------
# Button helpers
# ---------------------------------------------------------------------------

async def wait_button_press(button, timeout_ms):
    """
    Wait for a single button press (active-low).

    First drains any current press (waits for release), then waits for
    a new press.  Returns True on success, False on timeout.
    """
    start = time.ticks_ms()

    # If already pressed, wait for release first
    while button.value() == 0:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        await asyncio.sleep_ms(20)

    # Small settle delay after release
    await asyncio.sleep_ms(50)

    # Wait for new press
    while button.value() == 1:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        await asyncio.sleep_ms(20)

    return True


async def wait_button_release(button, timeout_ms):
    """Wait for button to be released. Returns True on success, False on timeout."""
    start = time.ticks_ms()
    while button.value() == 0:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        await asyncio.sleep_ms(20)
    return True


# ---------------------------------------------------------------------------
# DIP switch helper
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# RGB LED flash helper
# ---------------------------------------------------------------------------

async def flash_rgb(hw, r, g, b, count=3, on_ms=150, off_ms=100):
    """
    Flash the RGB LED `count` times in colour (r, g, b), each channel 0-255.

    Works with the common-anode LED wiring in hardware.py where
    duty_u16=0 is fully ON and duty_u16=65535 is fully OFF.
    """
    def _set(rv, gv, bv):
        hw["led_red"].duty_u16((255 - rv) * 257)
        hw["led_green"].duty_u16((255 - gv) * 257)
        hw["led_blue"].duty_u16((255 - bv) * 257)

    for _ in range(count):
        _set(r, g, b)
        await asyncio.sleep_ms(on_ms)
        _set(0, 0, 0)
        await asyncio.sleep_ms(off_ms)


async def wait_ready(hw, button):
    """
    Flash blue 3× then wait for USER BUTTON press+release (no timeout).
    Call at the start of every test to give the operator time to set up.
    """
    await flash_rgb(hw, 0, 0, 255, count=3)
    print("  Press USER BUTTON when ready to start…")
    # drain any held press
    while button.value() == 0:
        await asyncio.sleep_ms(20)
    # wait for press
    while button.value() == 1:
        await asyncio.sleep_ms(20)
    # wait for release
    while button.value() == 0:
        await asyncio.sleep_ms(20)
    await asyncio.sleep_ms(50)


async def flash_result(hw, passed):
    """Flash green 3× for PASS or red 5× for FAIL."""
    if passed:
        await flash_rgb(hw, 0, 255, 0, count=3, on_ms=200, off_ms=100)
    else:
        await flash_rgb(hw, 255, 0, 0, count=5, on_ms=200, off_ms=100)


async def wait_for_dip_pattern(hw, read_dip_fn, expected_bits, timeout_ms):
    """
    Wait until the DIP switches match expected_bits (e.g. "0101").

    Returns (address, True) on match, or (None, False) on timeout.
    """
    start = time.ticks_ms()
    while True:
        address, bits = read_dip_fn(hw)
        if bits == expected_bits:
            return address, True
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return None, False
        await asyncio.sleep_ms(100)
