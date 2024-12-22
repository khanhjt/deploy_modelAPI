import sys
import logging

from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from logging.handlers import RotatingFileHandler
from config.logging_cfg import LoggingConfig

class Logger:
    def __init__(self, name="", log_level=logging.INFO, log_file=None) -> None:
        self.log = logging.getLogger(name)
        self.get_logger(log_level, log_file)

    def get_logger(self, log_level, log_file):
        self.log.setLevel(log_level)
        self._init_formatter()
        if log_file is not None:
            self._add_file_hander(LoggingConfig.LOG_DIR / log_file)
        else:
            self._add_stream_hander()