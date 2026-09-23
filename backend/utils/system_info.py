import platform as plt
import socket as soc

def inf(prt, ver):
    try: ip = soc.gethostbyname(soc.gethostname())
    except OSError: ip = "127.0.0.1"
    return {"hostname": soc.gethostname(), "ip": ip, "port": prt, "protocol_version": ver, "os": plt.system(), "os_version": plt.release()}
# Glossary:
# inf = host information
# prt = port
# ver = protocol version
# ip = host IP
