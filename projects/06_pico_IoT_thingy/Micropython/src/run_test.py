"""
run_test.py — Run a single QC test from the REPL.

Usage:
    exec(open('run_test.py').read())

Shows a numbered menu; press the digit key to run that test.
"""

import sys
import asyncio
from lib.hardware import load_config, init_hardware

_TESTS = [
    ("rgb",    "tests.test_rgb",    "test_rgb_led"),
    ("button", "tests.test_button", "test_button"),
    ("dip",    "tests.test_dip",    "test_dip_switch"),
    ("i2c",    "tests.test_i2c",    "test_i2c_scan"),
    ("sht31",  "tests.test_sht31",  "test_sht31"),
    ("qwiic",  "tests.test_qwiic",  "test_qwiic"),
    ("relay",  "tests.test_relay",  "test_relay"),
    ("rs485",  "tests.test_rs485",  "test_rs485"),
    ("spi",    "tests.test_spi",    "test_spi"),
]

print("\nAvailable tests:")
for i, (name, _mod, _fn) in enumerate(_TESTS, 1):
    print(f"  {i}. {name}")
print("\nPress a digit key: ", end="")

ch = sys.stdin.readline().strip()

try:
    choice = int(ch)
except ValueError:
    choice = -1

if 1 <= choice <= len(_TESTS):
    key, module_path, fn_name = _TESTS[choice - 1]
    mod = __import__(module_path, None, None, [fn_name])
    test_fn = getattr(mod, fn_name)

    cfg   = load_config()
    hw    = init_hardware(cfg)
    state = {"current_test": key.upper(), "instructions": ""}

    print(f"\n--- Running test: {key.upper()} ---")
    result = asyncio.run(test_fn(hw, cfg, state))
    print(f"--- Result: {'PASS' if result else 'FAIL'} ---\n")
else:
    print(f"Invalid — choose 1–{len(_TESTS)}.")
