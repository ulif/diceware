import logging
from diceware.logger import logger, configure, NullHandler


def test_null_handler_removable():
    # the self-made NullHander is removable under py2.6
    my_logger = logging.getLogger('foo')
    handler = NullHandler()
    my_logger.addHandler(handler)
    assert len(my_logger.handlers) == 1
    my_logger.removeHandler(handler)
    assert len(my_logger.handlers) == 0


def test_logger_exists():
    # the logger does exist
    assert logger is not None


def test_logger_has_handler():
    # the logger has at least one handler
    configure(0)
    assert len(logger.handlers) > 0


def test_get_logger_by_name():
    # we can get a logger directly from std lib
    my_logger = logging.getLogger("ulif.diceware")
    configure(0)
    assert len(my_logger.handlers) > 0


def test_configure():
    # we can configure the logger.
    logger.setLevel(23)
    my_logger = logging.getLogger("ulif.diceware")
    configure(None)
    assert my_logger.level == 23
    configure(0)
    assert my_logger.level == logging.ERROR
    configure(1)
    assert my_logger.level == logging.INFO
    configure(2)
    assert my_logger.level == logging.DEBUG
