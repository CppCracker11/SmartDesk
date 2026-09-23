# Cross-Platform Support

The TCP server, UDP discovery, JSON protocol, framing, validation, pairing, session handling and dispatcher are platform-independent.

The OS-specific input layer is the adapter. Runtime selection chooses Windows, Linux or macOS without placing OS checks in networking or protocol code.

## Windows

`pynput` provides mouse, keyboard and media-key injection. Windows Firewall may need a Private-network rule for the host ports.

## Linux

Input injection is environment-dependent. X11 is the primary target. Wayland security policies can restrict synthetic input, so unsupported operations return `COMMAND_FAILED` instead of being reported as successful.

## macOS

Accessibility and/or Input Monitoring permissions may be required for mouse and keyboard injection. Media-key behavior can vary with OS permissions and desktop state.

## Keyboard modifiers

The protocol keeps `CTRL` and `CMD` as separate names. Windows/Linux map `CTRL` to the platform control key, while macOS can use `CMD` explicitly. The backend does not silently convert one protocol name into the other.

## Fallback behavior

If the local input backend is unavailable, SmartDesk can still start for protocol/network testing. Input commands return `COMMAND_FAILED`; they are not falsely reported as successful.

## Compatibility claim

SmartDesk uses one protocol across Windows, Linux and macOS. Identical behavior still depends on the host OS, desktop environment and permissions. Physical macOS behavior was not tested unless a macOS environment is available.
