"""
test_button.py — USER button test.

Asks the operator to press and release the USER button three times.
Uses timeout protection on every step.
"""

import asyncio
from lib.utils import wait_button_press, wait_button_release, wait_ready, flash_result

_REQUIRED_PRESSES = 3


async def test_button(hw, cfg, state):
    """
    Guide operator through three press/release cycles.
    Returns True on PASS, False on FAIL/timeout.
    """
    timeout_ms = cfg["timeouts"]["button"] * 1000
    button = hw["button"]

    await wait_ready(hw, button)
    print(f"  Press and release USER BUTTON {_REQUIRED_PRESSES} times.")
    print(f"  (timeout {cfg['timeouts']['button']} s per action)")

    for i in range(1, _REQUIRED_PRESSES + 1):
        # --- Wait for press ---
        state["instructions"] = f"Button: press #{i} of {_REQUIRED_PRESSES} — PRESS USER BUTTON"
        print(f"  [{i}/{_REQUIRED_PRESSES}] Press USER BUTTON…")

        if not await wait_button_press(button, timeout_ms):
            print(f"  TIMEOUT waiting for press #{i}.")
            state["instructions"] = f"Button: TIMEOUT on press #{i}"
            await flash_result(hw, False)
            return False

        print(f"  [{i}/{_REQUIRED_PRESSES}] Button pressed.")

        # --- Wait for release ---
        state["instructions"] = f"Button: press #{i} of {_REQUIRED_PRESSES} — RELEASE USER BUTTON"
        print(f"  [{i}/{_REQUIRED_PRESSES}] Release USER BUTTON…")

        if not await wait_button_release(button, timeout_ms):
            print(f"  TIMEOUT waiting for release #{i}.")
            state["instructions"] = f"Button: TIMEOUT on release #{i}"
            await flash_result(hw, False)
            return False

        print(f"  [{i}/{_REQUIRED_PRESSES}] Button released.")

    print("  All press/release cycles detected. Button OK.")
    await flash_result(hw, True)
    return True
