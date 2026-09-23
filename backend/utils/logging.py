import logging as lg

def log(lev):
    lg.basicConfig(level=getattr(lg, lev, lg.INFO), format="%(asctime)s | %(levelname)s | %(message)s")
    return lg.getLogger("smartdesk")
# Glossary:
# log = logging setup
# lev = log level
