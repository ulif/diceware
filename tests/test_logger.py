import logging
from diceware.logger import logger, configure


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


def test_configure():
    # we can configure the logger.
    my_logger = logging.getLogger("ulif.diceware")
    configure(None)
    assert my_logger.level == logging.NOTSET
    configure(0)
    assert my_logger.level == logging.CRITICAL
    configure(1)
    assert my_logger.level == logging.INFO
    configure(2)
    assert my_logger.level == logging.DEBUG
