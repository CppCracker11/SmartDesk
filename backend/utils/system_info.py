import platform
import socket


def get_local_ip() -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return "127.0.0.1"


def get_host_info(port: int, protocol_version: str) -> dict:
    return {
        "os": platform.system(),
        "os_version": platform.release(),
        "hostname": socket.gethostname(),
        "ip": get_local_ip(),
        "port": port,
        "protocol_version": protocol_version,
    }
