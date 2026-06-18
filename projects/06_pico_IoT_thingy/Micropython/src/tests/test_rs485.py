"""
test_rs485.py — RS485 UART echo test.

Sends a test string via UART0 (GPIO0/1, THVD1406 transceiver in
auto-direction mode) and waits for the echoed data back.

Requires either:
  - An RS485 echo dongle connected to the terminal block, OR
  - A PC running the echo helper script (see README.md)

The THVD1406 handles TX/RX direction automatically; no DE/RE GPIO
control is needed in firmware.
"""

import asyncio
import time
from lib.utils import wait_ready, flash_result

# How long to poll for the echo after transmitting (ms).
# At 9600 baud, 13-byte roundtrip via USB dongle ≈ 40 ms.
_RX_POLL_INTERVAL_MS = 5


async def test_rs485(hw, cfg, state):
    """
    Transmit a test string and validate the echoed response.
    Returns True on PASS, False on FAIL/timeout.
    """
    timeout_ms = cfg["timeouts"]["rs485"] * 1000
    uart      = hw["uart"]
    test_str  = cfg["rs485"]["test_string"]
    tx_bytes  = test_str.encode()
    button    = hw["button"]

    await wait_ready(hw, button)
    state["instructions"] = "RS485: sending echo test…"

    # Flush any stale RX data
    while uart.any():
        uart.read(uart.any())
        await asyncio.sleep_ms(10)

    print(f"  TX → {tx_bytes!r}")
    uart.write(tx_bytes)

    # Start polling immediately — THVD1406 auto-direction switches to RX
    # within ~1 character time (~1 ms at 9600 baud) after the last stop bit.
    # The USB-dongle roundtrip adds ~30-40 ms total, well within timeout.
    # Reading without a drain delay avoids discarding bytes that arrive early.
    start = time.ticks_ms()
    rx_buf = bytearray()

    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            chunk = uart.read(uart.any())
            if chunk:
                rx_buf += chunk
            # Stop as soon as we have at least as many bytes as we sent
            if len(rx_buf) >= len(tx_bytes):
                break
        await asyncio.sleep_ms(_RX_POLL_INTERVAL_MS)

    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print(f"  RX ← {bytes(rx_buf)!r}  ({elapsed} ms)")
    state["instructions"] = f"RS485 RX: {bytes(rx_buf)!r}"

    if not rx_buf:
        print("  No data received — check echo dongle / echo script.")
        await flash_result(hw, False)
        return False

    if rx_buf == tx_bytes:
        print("  Echo match ✓")
        await flash_result(hw, True)
        return True
    else:
        print("  Echo MISMATCH.")
        print(f"    Expected: {tx_bytes!r}")
        print(f"    Received: {bytes(rx_buf)!r}")
        await flash_result(hw, False)
        return False
