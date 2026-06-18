"""
web_server.py — Minimal async HTTP server for the QC web interface.

Serves a single auto-refreshing HTML page that shows the current test
state, instructions, per-test PASS/FAIL results, and the final board
verdict.  Plain HTML only; no JavaScript frameworks.
"""

import asyncio

# ---------------------------------------------------------------------------
# HTML page builder
# ---------------------------------------------------------------------------

_HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="5">
  <title>pico_IoT_thingy QC</title>
  <style>
    body  { font-family: monospace; background: #111; color: #ddd;
            padding: 24px; max-width: 600px; }
    h1    { color: #29abe2; margin-bottom: 4px; }
    h2    { color: #aaa; font-size: 1em; margin-top: 20px; }
    .cur  { color: #ffdd00; font-weight: bold; }
    .inst { color: #ccc; font-style: italic; }
    table { border-collapse: collapse; margin-top: 8px; width: 100%; }
    td    { padding: 4px 12px; border-bottom: 1px solid #333; }
    td:first-child { width: 60%; }
    .pass { color: #3ddc84; font-weight: bold; }
    .fail { color: #ff5252; font-weight: bold; }
    .summary { margin-top: 20px; font-size: 1.4em; font-weight: bold; }
    hr    { border-color: #333; }
  </style>
</head>
<body>
<h1>pico_IoT_thingy &mdash; Manufacturing QC</h1>
<hr>
"""

_HTML_FOOT = """
<p style="color:#555;font-size:0.8em;">Page auto-refreshes every 5 s.</p>
</body></html>
"""


def _build_html(state):
    """Render the full HTML page from the current shared state dict."""
    current = state.get("current_test", "—")
    instructions = state.get("instructions", "")
    results = state.get("results", {})
    final = state.get("final_result")

    body = _HTML_HEAD
    body += f'<h2>Current test</h2>\n<p class="cur">{current}</p>\n'
    body += f'<h2>Instructions</h2>\n<p class="inst">{instructions}</p>\n'

    if results:
        body += "<h2>Results</h2>\n<table>\n"
        for name, passed in results.items():
            css = "pass" if passed else "fail"
            label = "PASS" if passed else "FAIL"
            body += f'  <tr><td>{name}</td><td class="{css}">{label}</td></tr>\n'
        body += "</table>\n"

    if final is not None:
        css = "pass" if final == "PASS" else "fail"
        body += f'<p class="summary">BOARD RESULT: <span class="{css}">{final}</span></p>\n'

    body += _HTML_FOOT
    return body


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

async def _handle_client(reader, writer, state):
    """Handle a single HTTP request; always returns the status page."""
    try:
        # Consume request headers (we only serve one page regardless of path)
        try:
            await asyncio.wait_for(reader.readline(), timeout=3)
            while True:
                line = await asyncio.wait_for(reader.readline(), timeout=2)
                if line in (b"\r\n", b""):
                    break
        except asyncio.TimeoutError:
            pass

        body = _build_html(state)
        body_bytes = body.encode("utf-8")
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        writer.write(header.encode() + body_bytes)
        await writer.drain()
    except Exception:
        pass  # Silently ignore broken connections
    finally:
        writer.close()
        await writer.wait_closed()


# ---------------------------------------------------------------------------
# Server entry point
# ---------------------------------------------------------------------------

async def run_server(state, port=80):
    """
    Start the HTTP server and keep it running until the event loop stops.

    Call as an asyncio task:
        asyncio.create_task(run_server(state))
    """
    server = await asyncio.start_server(
        lambda r, w: _handle_client(r, w, state),
        "0.0.0.0",
        port,
    )
    print(f"[WEB] HTTP server listening on port {port}")
    await server.wait_closed()
