# Setup

1. Install Python 3.10 or newer.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Put the host and Android controller on the same trusted LAN.
4. Start the host with `python -m backend.main`.
5. Use UDP discovery or manually connect to the host TCP IP/port.
6. Enter the temporary pairing code printed by the host.

## Windows

Run `scripts/run_windows.bat`. Allow Python on the Private network if Windows Firewall prompts.

## Linux

Run `scripts/run_linux.sh`. Test input injection on X11 first. Wayland may restrict synthetic input.

## macOS

Run `scripts/run_macos.sh`. Grant the terminal/Python process the required Accessibility/Input Monitoring permissions when prompted.

## Ports

TCP 8765 is the command channel. UDP 8766 is discovery. Both can be changed with environment variables.
