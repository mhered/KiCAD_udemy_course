"""
test_relay.py — Relay test.

Toggles the relay ON/OFF three times.
Asks the operator to confirm relay clicks and yellow OUT LED via
the USER button.

NOTE: The relay NO/NC silkscreen labels on the PCB are incorrect;
this test only validates that the relay activates.
"""

import asyncio
from lib.utils import wait_button_press, wait_ready, flash_result

_CYCLES = 3
_OFF_MS = 600   # pause (ms) after relay de-energises before next cycle


async def test_relay(hw, cfg, state):
    """
    Toggle relay three times then request operator confirmation.
    Returns True on PASS, False on FAIL/timeout.
    """
    timeout_ms = cfg["timeouts"]["relay"] * 1000
    relay  = hw["relay"]
    button = hw["button"]

    await wait_ready(hw, button)
    print(f"  Toggling relay {_CYCLES} times — press USER BUTTON each time to advance.")
    print("  Measure voltages / listen for clicks while relay is held ON.")

    for i in range(1, _CYCLES + 1):
        # --- ON: hold until operator presses button ---
        state["instructions"] = (
            f"Relay cycle {i}/{_CYCLES}: ENERGISED — measure voltages, "
            "then press USER BUTTON to de-energise."
        )
        print(f"  Cycle {i}/{_CYCLES}: ON — press USER BUTTON when done measuring.")
        relay.value(1)
        ok = await wait_button_press(button, timeout_ms)
        if not ok:
            print("  TIMEOUT waiting for confirmation (relay ON).")
            relay.value(0)
            await flash_result(hw, False)
            return False

        # --- OFF: brief pause so operator can observe de-energised state ---
        state["instructions"] = f"Relay cycle {i}/{_CYCLES}: DE-ENERGISED"
        print(f"  Cycle {i}/{_CYCLES}: OFF")
        relay.value(0)
        await asyncio.sleep_ms(_OFF_MS)

    state["instructions"] = (
        "Did you hear all relay clicks and see the OUT LED? "
        "Press USER BUTTON to confirm PASS."
    )
    print("  Press USER BUTTON to confirm relay clicks and OUT LED were observed.")
    print(f"  (timeout {cfg['timeouts']['relay']} s)")

    passed = await wait_button_press(button, timeout_ms)

    if passed:
        print("  Operator confirmed: relay OK.")
    else:
        print("  TIMEOUT — no confirmation received.")

    relay.value(0)  # Safety: ensure relay is off on exit
    await flash_result(hw, passed)
    return passed
