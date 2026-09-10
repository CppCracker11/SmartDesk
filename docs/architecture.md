# SmartDesk Architecture

## Data flow

```text
Controller
   |
   | TCP JSON messages
   v
Connection Manager
   |
   +--> Authentication / Session
   |
   v
Protocol Parser + Validator
   |
   v
Command Dispatcher
   |
   v
OSAdapter interface
   |-------- WindowsAdapter
   |-------- LinuxAdapter
   \-------- MacOSAdapter
```

UDP discovery is separate from command transport. A controller broadcasts `SMARTDESK_DISCOVER` on UDP port 8766. A host answers with its hostname, IP, TCP port and protocol version. If UDP discovery fails, the controller can connect directly using the host IP.

## Why this structure?

The network layer knows nothing about mouse APIs. The dispatcher knows only generic command types. The OS adapter is the only layer that knows how local input is generated. This keeps the protocol identical for Windows, Linux and macOS.

## Async model

The host uses `asyncio` because network I/O is mostly waiting: accepting connections, receiving bytes and sending responses. This keeps the server responsive without creating a thread for every client. The input library performs the small local input operation when a command is dispatched.

## Connection states

- CONNECTING — TCP connection is being established.
- CONNECTED — TCP connection exists.
- AUTHENTICATING — host is waiting for pairing or session resume.
- AUTHENTICATED — commands may be executed.
- DISCONNECTED — connection is closed.

A session token survives a TCP reconnect for its configured session lifetime, allowing a controller to resume without reusing the pairing code.
