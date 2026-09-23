import os as os

HST = os.getenv("SMARTDESK_HOST", "0.0.0.0")
PRT = int(os.getenv("SMARTDESK_PORT", "8765"))
DPT = int(os.getenv("SMARTDESK_DISCOVERY_PORT", "8766"))
PTO = int(os.getenv("SMARTDESK_PAIRING_TIMEOUT", "120"))
STO = int(os.getenv("SMARTDESK_SESSION_TIMEOUT", "3600"))
LOG = os.getenv("SMARTDESK_LOG_LEVEL", "INFO").upper()
VER = "1.0"
