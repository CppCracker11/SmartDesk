# Cross-Platform Support

## Platform-independent parts

The TCP server, UDP discovery, JSON protocol, message framing, validation, pairing, session handling, command dispatcher and tests are written without operating-system-specific command names.

## OS-specific part

Only the `OSAdapter` implementation performs local input injection:

- `WindowsAdapter`
- `LinuxAdapter`
- `MacOSAdapter`

Runtime selection uses `platform.system()` and maps `Windows`, `Linux` and `Darwin` to the corresponding adapter.

## Windows

Windows is the primary mandatory desktop target. `pynput` provides mouse and keyboard injection and exposes media-key controls.

## Linux

Linux desktop input is environment-dependent. X11 is the safest target for this project. Wayland deliberately restricts synthetic input from ordinary applications, so SmartDesk cannot honestly promise identical behavior on every Wayland compositor. Test on the exact distribution and desktop environment used for the demonstration.

## macOS

macOS has privacy protections around input injection. The Python process may need Accessibility and/or Input Monitoring permissions in System Settings. The adapter exists in this version, but permissions and OS-version differences can affect results.

## Honest compatibility claim

SmartDesk provides one protocol and three host adapters. That is cross-OS architectural compatibility. It does not mean every command behaves identically on every desktop environment without setup or permissions.
