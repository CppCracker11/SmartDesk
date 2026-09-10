import logging
import sys


def setup_logging(level: str) -> logging.Logger:
    logger = logging.getLogger("smartdesk")
    logger.setLevel(getattr(logging, level, logging.INFO))
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
    return logger
