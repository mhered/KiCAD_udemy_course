# rs485_echo.py  — run on PC
# Usage: python rs485_echo.py [PORT]
#   PORT  serial port (e.g. /dev/ttyUSB0, COM3) — omit or pass "auto" to detect

import sys
import glob
import subprocess
import serial


BAUD = 9600


def _usb_serial_candidates_linux():
    """Return a list of (port, description) for likely USB-serial adapters."""
    candidates = []

    # Grab kernel USB serial devices via sysfs + udevadm for description
    tty_paths = sorted(
        glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    )
    for port in tty_paths:
        desc = port
        try:
            result = subprocess.run(
                ["udevadm", "info", "--query=property", f"--name={port}"],
                capture_output=True, text=True, timeout=2,
            )
            props = {}
            for line in result.stdout.splitlines():
                if "=" in line:
                    k, _, v = line.partition("=")
                    props[k.strip()] = v.strip()
            vendor = props.get("ID_VENDOR_FROM_DATABASE") or props.get("ID_VENDOR", "")
            model  = props.get("ID_MODEL_FROM_DATABASE")  or props.get("ID_MODEL",  "")
            vid    = props.get("ID_VENDOR_ID", "")
            pid    = props.get("ID_MODEL_ID", "")
            parts  = [p for p in (vendor, model) if p]
            if parts:
                desc = f"{port}  [{', '.join(parts)}  VID:PID={vid}:{pid}]"
            else:
                desc = f"{port}  [VID:PID={vid}:{pid}]" if vid else port
        except Exception:
            pass
        candidates.append((port, desc))
    return candidates


def pick_port_auto():
    candidates = _usb_serial_candidates_linux()
    if not candidates:
        print("No USB serial devices found (/dev/ttyUSB*, /dev/ttyACM*).")
        print("Connect the RS485 dongle and retry, or pass the port explicitly.")
        sys.exit(1)

    print("USB serial devices found:")
    for i, (_, desc) in enumerate(candidates):
        print(f"  [{i}] {desc}")

    if len(candidates) == 1:
        port, desc = candidates[0]
        ans = input(f"Use {desc}? [Y/n] ").strip().lower()
        if ans in ("", "y", "yes"):
            return port
        print("Aborted.")
        sys.exit(0)

    while True:
        raw = input(f"Select device [0-{len(candidates)-1}] or 'q' to quit: ").strip().lower()
        if raw == "q":
            print("Aborted.")
            sys.exit(0)
        try:
            idx = int(raw)
            if 0 <= idx < len(candidates):
                return candidates[idx][0]
        except ValueError:
            pass
        print("  Invalid choice, try again.")


def resolve_port(arg):
    if not arg or arg.lower() == "auto":
        return pick_port_auto()
    return arg


if __name__ == "__main__":
    port_arg = sys.argv[1] if len(sys.argv) > 1 else "auto"
    PORT = resolve_port(port_arg)

    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print(f"RS485 echo on {PORT} @ {BAUD} baud — Ctrl+C to stop")
        try:
            while True:
                data = ser.read(64)
                if data:
                    print(f"  Echo: {data!r}")
                    ser.write(data)
        except KeyboardInterrupt:
            print("\nStopped.")