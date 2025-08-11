import logging

# Configure logger only once
_logger = logging.getLogger("main_logger")
_logger.setLevel(logging.INFO)

if not _logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

# This is what you'll import
def log(message, level="info"):
    level = level.lower()
    if level == "debug":
        _logger.debug(message)
    elif level == "warning":
        _logger.warning(message)
    elif level == "error":
        _logger.error(message)
    elif level == "critical":
        _logger.critical(message)
    else:
        _logger.info(message)
