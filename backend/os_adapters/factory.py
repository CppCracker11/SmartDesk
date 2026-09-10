import platform

from .linux import LinuxAdapter
from .macos import MacOSAdapter
from .windows import WindowsAdapter


def create_adapter():
    system = platform.system()
    if system == "Windows":
        return WindowsAdapter()
    if system == "Linux":
        return LinuxAdapter()
    if system == "Darwin":
        return MacOSAdapter()
    raise RuntimeError(f"Unsupported operating system: {system}")
