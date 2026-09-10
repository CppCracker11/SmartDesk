# Setup Guide

## All platforms

1. Install Python 3.10+.
2. Open a terminal in the SmartDesk directory.
3. Run `python -m pip install -r requirements.txt`.
4. Make sure host and controller are on the same LAN.
5. Start the host with `python -m backend.main`.

## Windows

Run `scripts\\run_windows.bat` or `python -m backend.main`.

Allow Python through the Windows firewall for Private networks when Windows asks. Do not expose the port to Public networks unless you understand the risk.

## Linux

Install Tkinter if needed. On Debian/Ubuntu-like systems this is commonly provided by the `python3-tk` package. Install any input-system packages required by `pynput` for your desktop environment.

For reliable input injection, test on an X11 session. Wayland may restrict synthetic input.

Run `./scripts/run_linux.sh`.

## macOS

Run `./scripts/run_macos.sh`. If mouse/keyboard injection is denied, open System Settings > Privacy & Security and grant the required Accessibility/Input Monitoring permissions to the terminal or Python application being used.

## Firewall and Wi-Fi isolation

Discovery uses UDP 8766 and control uses TCP 8765 by default. A firewall or Wi-Fi access point with client isolation can block either. Manual IP connection helps diagnose discovery-specific failures.
