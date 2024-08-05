import logging
import logging.handlers
from datetime import datetime


def set_logger(name):
    """
    Method to set file and stream handler and generate log file.
    log file will generate at current folder with name "log-<YYMMDD_HHMMSS>.log"
    """
    filename_startswith = 'log-'
    _logger = logging.getLogger(name or __name__)
    _logger.setLevel(logging.INFO)

    # File handler to move stdout to log file
    log_file_name = filename_startswith + datetime.now().strftime("%y%m%d_%H%M%S") + ".log"
    file_handler = logging.handlers.RotatingFileHandler(log_file_name)
    file_format = logging.Formatter("%(asctime)s [%(levelname)s]: %(name)s: %(message)s")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)

    # Removing the stream handler to avoid printing to console
    for handler in _logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            _logger.removeHandler(handler)

    # Adding only the file handler
    _logger.addHandler(file_handler)
    return _logger
