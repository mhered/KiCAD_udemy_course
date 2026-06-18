"""
test_spi.py — SPI loopback test.

Sends four test bytes and verifies the received bytes match.

Requires MOSI (GPIO3) and MISO (GPIO4) to be externally shorted
with a jumper or test jig (see README.md).
"""

import asyncio
from lib.utils import wait_ready, flash_result

_TX_BYTES = bytes([0x55, 0xAA, 0xDE, 0xAD])


async def test_spi(hw, cfg, state):
    """
    SPI loopback: transmit _TX_BYTES and verify echo on MISO.
    Returns True on PASS, False on FAIL.
    """
    state["instructions"] = "SPI loopback test… (MOSI–MISO shorted?)"
    button = hw["button"]

    await wait_ready(hw, button)
    print("  Ensure MOSI (GPIO3) and MISO (GPIO4) are shorted.")
    print(f"  TX → {list(hex(b) for b in _TX_BYTES)}")

    rx = bytearray(len(_TX_BYTES))

    try:
        hw["spi_cs"].value(0)
        hw["spi"].write_readinto(_TX_BYTES, rx)
        hw["spi_cs"].value(1)
    except Exception as e:
        hw["spi_cs"].value(1)
        print(f"  SPI error: {e}")
        state["instructions"] = f"SPI error: {e}"
        await flash_result(hw, False)
        return False

    print(f"  RX ← {list(hex(b) for b in rx)}")

    if rx == bytearray(_TX_BYTES):
        print("  Loopback match ✓")
        state["instructions"] = "SPI loopback: PASS"
        await flash_result(hw, True)
        return True
    else:
        print("  Loopback MISMATCH.")
        print(f"    Expected: {list(hex(b) for b in _TX_BYTES)}")
        print(f"    Received: {list(hex(b) for b in rx)}")
        state["instructions"] = "SPI loopback: FAIL — data mismatch"
        await flash_result(hw, False)
        return False
