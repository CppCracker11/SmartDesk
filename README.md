# SmartDesk

SmartDesk is a cross-platform LAN productivity controller. An Android controller can send versioned JSON commands over TCP to a host computer. The host validates, authenticates and dispatches commands through a platform adapter.

## Included

- TCP with newline-delimited JSON framing
- Explicit connection/authentication lifecycle
- One-time six-digit pairing code
- Session token resume after temporary disconnect until session expiry
- One active authenticated controller per host
- UDP LAN discovery with manual IP/port fallback
- Mouse, keyboard, media and presentation commands
- Windows, Linux and macOS adapters through `pynput`
- Ping/pong timestamps for client-side RTT measurement
- Standard-library tests
- Small command-line backend test client

## Run

Python 3.10+ is required.

```bash
python -m pip install -r requirements.txt
python -m backend.main
```

The host listens on TCP `8765` and UDP `8766` by default and prints the temporary pairing code.

Environment variables:

- `SMARTDESK_HOST`
- `SMARTDESK_PORT`
- `SMARTDESK_DISCOVERY_PORT`
- `SMARTDESK_PAIRING_TIMEOUT`
- `SMARTDESK_SESSION_TIMEOUT`
- `SMARTDESK_LOG_LEVEL`

## Test

```bash
python -m unittest discover -s tests -v
```

## Test client

```bash
python test_client/client.py
```

It connects to the host, pairs, and can exercise ping, host information, mouse movement and keyboard press/release. It is only a backend test tool, not the Android application.

## Protocol

Transport is TCP. Each message is one UTF-8 JSON object terminated by `\n`.

```json
{"version":"1.0","id":"abc123","type":"mouse","action":"move","data":{"dx":10,"dy":-4},"token":"..."}
```

Authentication:

1. Connect.
2. Send `auth/pair` with the six-digit code.
3. Receive a session token.
4. Include the token in later commands.
5. If TCP temporarily disconnects, use `auth/resume` with the same token after reconnecting.
6. A valid token and an active TCP connection are separate states; a temporary disconnect does not immediately expire the session.

Commands are rejected until authentication succeeds.

## Platform notes

- Windows: `pynput` uses the local input system. Windows may ask for firewall permission for the private LAN.
- Linux: synthetic input normally works best on X11. Wayland desktop security can restrict it.
- macOS: Accessibility/Input Monitoring permissions may be required.
- Media keys vary by platform/desktop environment; unsupported operations return `COMMAND_FAILED` instead of being reported as successful.

## Network/security scope

This is a trusted-LAN prototype. TCP is the command channel and UDP is only discovery. The host is not designed to be exposed directly to the public Internet and does not implement TLS, cloud infrastructure, screen streaming, file transfer or remote desktop features.

## Structure

```text
SmartDesk/
  backend/
    commands/
    network/
    os_adapters/
    protocol/
    security/
    utils/
  test_client/
  tests/
  docs/
  scripts/
  requirements.txt
```
