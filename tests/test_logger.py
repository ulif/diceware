from diceware.logger import logger


def test_logger_exists():
    # the logger does exist
    assert logger is not None


def test_logger_has_handler():
    # the logger has at least one handler
    assert len(logger.handlers) > 0
