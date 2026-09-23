# SmartDesk Architecture

```text
Android / Test Client
        |
        | TCP + newline JSON
        v
      Host
        |
        +-- Connection lifecycle
        +-- Pairing / session
        +-- Protocol parser + validator
        +-- Command dispatcher
        |
        v
   OS Adapter
    /   |   \
 Win   Lin   Mac

UDP discovery is separate from the TCP command channel.
```

## Connection lifecycle

`CONNECTING` → `CONNECTED` → `ACTIVE` → `DISCONNECTED`. Authentication creates a valid session token; `ACTIVE` means that token is currently bound to a live TCP connection.

A session token can survive a TCP reconnect until its configured session timeout. Only one authenticated controller is active at a time.

## Network model

`asyncio` handles TCP and UDP I/O. TCP uses newline-delimited JSON framing. UDP is only a LAN convenience for discovery; manual host IP and TCP port are always supported.

## OS abstraction

The dispatcher sends generic operations to one adapter interface. Windows/Linux/macOS translation stays inside the adapter modules. This keeps OS checks out of networking and protocol code.

## Failure handling

Malformed input, unsupported protocol versions, invalid commands, expired sessions, busy hosts and unavailable OS input backends produce explicit error responses. Client input must not terminate the host process.
