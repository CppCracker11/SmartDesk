# SmartDesk

SmartDesk is a small cross-platform LAN productivity controller. A controller sends structured JSON commands over TCP to a host computer. The host authenticates the controller, validates commands, dispatches them, and translates them through an OS adapter.

## Features

- TCP client-server communication
- Newline-delimited JSON message framing
- UDP LAN discovery with manual IP fallback
- One-time six-digit pairing code
- Session token authentication and reconnect/resume
- Mouse, keyboard, media and presentation commands
- Windows, Linux and macOS adapter modules
- Host information and ping latency measurement
- Beginner-friendly modular code
- Standard-library test suite
- Temporary Tkinter test client

## Architecture

```text
Controller / Test Client
        |
        | LAN TCP + UDP discovery
        v
SmartDesk Server
        |
        +-- Connection Manager
        +-- Pairing / Session
        +-- Protocol Parser + Validator
        +-- Command Dispatcher
        |
        v
     OSAdapter
     /   |   \
Windows Linux macOS
```

The application protocol is platform-independent. Only the OS adapter translates generic commands into local input events.

## Requirements

- Python 3.10 or newer
- `pynput==1.8.2`
- Tkinter for the temporary GUI client (normally included with desktop Python; some Linux distributions package it separately)

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the host

From the SmartDesk directory:

```bash
python -m backend.main
```

The server prints a six-digit pairing code. Default ports are TCP `8765` and UDP discovery `8766`.

Configuration can be changed with environment variables:

```text
SMARTDESK_HOST
SMARTDESK_PORT
SMARTDESK_DISCOVERY_PORT
SMARTDESK_PAIRING_TIMEOUT
SMARTDESK_LOG_LEVEL
```

## Run the temporary client

From the SmartDesk directory:

```bash
python test_client/client.py
```

Use **Discover** on the same LAN, or type the host IP and port manually. Then connect and enter the pairing code shown by the host.

## Testing

Run:

```bash
python -m unittest discover -s tests -v
```

The tests cover message framing, validation, pairing, session tokens, dispatcher routing, a real loopback TCP ping, and pairing/resume on the SmartDesk server.

## Protocol summary

Every application message is one JSON object followed by `\\n`.

```json
{
  "version": "1.0",
  "id": "12345",
  "type": "mouse",
  "action": "move",
  "data": {"dx": 12, "dy": -5},
  "token": "..."
}
```

Responses contain the same `id` and either `status: ok` or `status: error`.

See `docs/protocol.md` for the complete command contract.

## Security notes

SmartDesk is a prototype intended primarily for a trusted local network. Pairing is not a replacement for TLS. Commands are explicitly whitelisted and arbitrary shell execution is not supported. Do not expose the server directly to the public Internet.

## Known limitations

- Linux input injection depends on the desktop/input backend. X11 is the primary supported Linux configuration. Wayland security policies may prevent or limit synthetic input.
- macOS requires appropriate Accessibility/Input Monitoring permissions depending on the operation and macOS version.
- Media-key behavior can vary by desktop environment and application.
- The temporary GUI is intentionally simple and is not the final mobile controller.
- Discovery can be blocked by a firewall or Wi-Fi client isolation; manual IP entry remains available.
- The prototype does not provide TLS, cloud connectivity, screen streaming, clipboard synchronization, or file transfer.

## Project documentation

- `docs/architecture.md` — component architecture
- `docs/protocol.md` — application protocol and commands
- `docs/cross_platform.md` — OS adapter and platform limitations
- `docs/networking_concepts.md` — Computer Networks concepts demonstrated
- `docs/setup.md` — platform setup
- `docs/testing.md` — test and demo procedure

## Future scope

QR pairing, clipboard synchronization, file transfer, macros, richer host telemetry, and a polished mobile application can be added later without changing the core command model.
