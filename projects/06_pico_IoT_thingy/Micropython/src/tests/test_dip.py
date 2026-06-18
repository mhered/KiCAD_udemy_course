"""
test_dip.py — DIP switch test.

Guides the operator through six switch patterns, one at a time.
Each pattern exercises a different combination of switches to verify
that every switch and GPIO trace is functional.

For each step the expected MODBUS address is also displayed.
"""

import asyncio
from lib.hardware import read_dip
from lib.utils import wait_for_dip_pattern, wait_ready, flash_result

# (label, expected_bits, expected_address)
# Bit order: DIP4 DIP3 DIP2 DIP1  (DIP1 = LSB)
_PATTERNS = [
    ("0001", "0001",  1),
    ("0010", "0010",  2),
    ("0100", "0100",  4),
    ("1000", "1000",  8),
    ("1111", "1111", 15),
    ("0000", "0000",  0),
]


async def test_dip_switch(hw, cfg, state):
    """
    Step through DIP switch patterns; detect each pattern in turn.
    Returns True if all six patterns are matched, False on any timeout.
    """
    timeout_ms = cfg["timeouts"]["dip_switch"] * 1000
    button = hw["button"]

    await wait_ready(hw, button)
    print("  Follow the instructions to set each DIP switch pattern.")
    print(f"  (timeout {cfg['timeouts']['dip_switch']} s per step)")
    print("  DIP positions: [DIP4 DIP3 DIP2 DIP1]  1=ON  0=OFF")

    for label, expected_bits, expected_addr in _PATTERNS:
        state["instructions"] = (
            f"DIP: set pattern [{label}]  "
            f"→ MODBUS addr {expected_addr}"
        )
        print(f"\n  Set DIP switches to [{label}]  "
              f"(MODBUS address {expected_addr})…")

        address, ok = await wait_for_dip_pattern(hw, read_dip, expected_bits, timeout_ms)

        if not ok:
            # Show what we actually see on timeout
            current_addr, current_bits = read_dip(hw)
            print(f"  TIMEOUT. Last reading: [{current_bits}] = address {current_addr}")
            state["instructions"] = f"DIP: TIMEOUT on pattern [{label}]"
            await flash_result(hw, False)
            return False

        print(f"  Pattern [{label}] detected — MODBUS address {address}")

    print("  All DIP switch patterns verified.")
    await flash_result(hw, True)
    return True
