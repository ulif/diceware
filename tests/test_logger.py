import logging
from diceware.logger import logger


def test_logger_exists():
    # the logger does exist
    assert logger is not None


def test_logger_has_handler():
    # the logger has at least one handler
    assert len(logger.handlers) > 0


def test_get_logger_by_name():
    # we can get a logger directly from std lib
    my_logger = logging.getLogger("ulif.diceware")
    assert len(my_logger.handlers) > 0
