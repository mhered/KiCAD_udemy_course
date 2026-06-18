"""
main.py — pico_IoT_thingy Manufacturing QC Firmware
=====================================================

Entry point.  Runs the full test sequence while simultaneously serving
a status web page over WiFi (if available).

Architecture:
  - asyncio event loop drives both the test runner and the HTTP server.
  - All tests are async coroutines so the web server stays responsive
    during button-wait and timeout periods.
  - USB CDC serial (print) is the primary operator interface.
  - UART0 is reserved exclusively for RS485 testing.

File layout on Pico flash:
  /main.py
  /config/board_config.py
  /config/secrets.py
  /lib/hardware.py
  /lib/utils.py
  /lib/web_server.py
  /tests/test_rgb.py  test_button.py  test_dip.py
         test_i2c.py  test_sht31.py   test_qwiic.py
         test_relay.py test_rs485.py  test_spi.py
"""

import time
import asyncio

# ---------------------------------------------------------------------------
# Firmware identity
# ---------------------------------------------------------------------------

_FIRMWARE_VERSION = "1.0.0"
_BOARD_NAME       = "pico_IoT_thingy"

# ---------------------------------------------------------------------------
# Shared state — updated by tests, read by the web server
# ---------------------------------------------------------------------------

state = {
    "current_test":  "Startup",
    "instructions":  "Initialising…",
    "results":       {},
    "final_result":  None,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _halt():
    """Stop execution without triggering a soft reboot."""
    print("[HALT] Firmware halted. Reset the board to retry.")
    while True:
        await asyncio.sleep(60)


def print_banner():
    print(f"  {_BOARD_NAME}  QC Firmware  v{_FIRMWARE_VERSION}")
    print("=" * 52)
    print()


def print_summary(results):
    print()
    print("=" * 52)
    print("  FINAL TEST SUMMARY")
    print("=" * 52)
    all_pass = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {name:<22} {status}")
        if not passed:
            all_pass = False
    print("=" * 52)
    verdict = "PASS" if all_pass else "FAIL"
    print(f"  BOARD RESULT: {verdict}")
    print("=" * 52)
    print()
    return verdict


async def connect_wifi():
    """
    Attempt WiFi connection.  Returns IP string on success, None on failure.
    Credentials are loaded from config/secrets.py (not tracked in git).
    Failure is non-fatal; the firmware continues over USB serial only.
    """
    try:
        import network
    except ImportError:
        print("[WIFI] network module not available (non-W Pico?).")
        return None

    try:
        from config.secrets import WIFI_SSID as ssid, WIFI_PASSWORD as password
    except ImportError:
        print("[WIFI] config/secrets.py not found — skipping WiFi.")
        print("       Copy config/secrets.example.py to config/secrets.py and set credentials.")
        return None

    try:
        wlan = network.WLAN(network.STA_IF)
        # CYW43 sometimes needs a moment after boot — retry up to 3 times
        for _attempt in range(3):
            try:
                wlan.active(True)
                break
            except OSError:
                await asyncio.sleep_ms(600)
        else:
            print("[WIFI] CYW43 failed to initialise — skipping WiFi.")
            return None
        wlan.connect(ssid, password)

        print(f"[WIFI] Connecting to '{ssid}'", end="")
        deadline = time.ticks_add(time.ticks_ms(), 15_000)
        while not wlan.isconnected():
            if time.ticks_diff(deadline, time.ticks_ms()) <= 0:
                print(" timeout.")
                return None
            await asyncio.sleep_ms(400)   # yield — keeps event loop responsive
            print(".", end="")

        ip = wlan.ifconfig()[0]
        print(f" connected.\n[WIFI] IP address: {ip}")
        return ip

    except Exception as exc:
        print(f"\n[WIFI] Error: {exc}")
        return None


# ---------------------------------------------------------------------------
# Test registry — order defines execution sequence
# ---------------------------------------------------------------------------

_TESTS = [
    ("RGB_LED",    "tests.test_rgb",    "test_rgb_led"),
    ("BUTTON",     "tests.test_button", "test_button"),
    ("DIP_SWITCH", "tests.test_dip",    "test_dip_switch"),
    ("I2C",        "tests.test_i2c",    "test_i2c_scan"),
    ("SHT31",      "tests.test_sht31",  "test_sht31"),
    ("QWIIC",      "tests.test_qwiic",  "test_qwiic"),
    ("RELAY",      "tests.test_relay",  "test_relay"),
    ("RS485",      "tests.test_rs485",  "test_rs485"),
    ("SPI",        "tests.test_spi",    "test_spi"),
]


def _import_test(module_path, fn_name):
    """Dynamically import and return a test function."""
    # MicroPython's __import__ with fromlist mimics 'from pkg import mod'
    parts = module_path.rsplit(".", 1)
    if len(parts) == 2:
        pkg, mod = parts
        m = __import__(module_path, None, None, [fn_name])
    else:
        m = __import__(module_path)
    return getattr(m, fn_name)


# ---------------------------------------------------------------------------
# Main async entry point
# ---------------------------------------------------------------------------

async def run_tests(hw, cfg):
    """Execute all tests in sequence; update shared state throughout."""
    for test_name, module_path, fn_name in _TESTS:
        state["current_test"] = test_name
        state["instructions"] = f"Running {test_name}…"

        print(f"\n{'─' * 52}")
        print(f"  TEST: {test_name}")
        print(f"{'─' * 52}")

        try:
            test_fn = _import_test(module_path, fn_name)
            result  = await test_fn(hw, cfg, state)
        except Exception as exc:
            print(f"  [ERROR] Unhandled exception in {test_name}: {exc}")
            result = False

        state["results"][test_name] = result
        status = "PASS" if result else "FAIL"
        print(f"\n  ► {test_name}: {status}")

    # Summary
    verdict = print_summary(state["results"])
    state["current_test"] = "COMPLETE"
    state["final_result"] = verdict
    state["instructions"] = f"All tests done — Board: {verdict}"


async def main():
    print_banner()

    # Import hardware module once
    from lib.hardware import load_config, init_hardware

    # --- Load configuration -------------------------------------------------
    print("[INIT] Loading config…")
    try:
        cfg = load_config()
    except Exception as exc:
        print(f"[FATAL] Cannot load config: {exc}")
        print("        Deploy all files first: uv run mpremote fs cp -r src/. :")
        await _halt()

    # --- Initialise hardware ------------------------------------------------
    print("[INIT] Initialising hardware…")
    try:
        hw = init_hardware(cfg)
    except Exception as exc:
        print(f"[FATAL] Hardware init failed: {exc}")
        await _halt()

    print("[INIT] Hardware ready.")

    # --- WiFi + web server --------------------------------------------------
    ip = await connect_wifi()

    if ip:
        from lib.web_server import run_server
        asyncio.create_task(run_server(state, port=80))
        state["instructions"] = f"Web interface: http://{ip}"
        print(f"[WEB]  Open http://{ip} in a browser.")
    else:
        print("[WEB]  No web interface — running USB serial only.")

    # Small delay so the web server task can start before tests begin
    await asyncio.sleep_ms(200)

    # --- Run test sequence --------------------------------------------------
    await run_tests(hw, cfg)

    # --- Keep web server alive after tests finish ---------------------------
    if ip:
        print("[WEB]  Tests complete. Web server still serving results.")
        print("       Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(5)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[EXIT] Interrupted by user.")
