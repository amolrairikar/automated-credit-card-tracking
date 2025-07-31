import io
import logging
import sys
from unittest.mock import MagicMock, patch

from api.utils.setup_logger import setup_logger


def test_setup_logger_returns_correct_name_and_level():
    """Tests that setup_logger returns a logger with the name and level specified in
    the function call."""
    logger_name = "test_logger"
    level = logging.DEBUG
    logger = setup_logger(logger_name=logger_name, level=level)
    assert logger.name == logger_name
    assert logger.level == level


@patch("logging.StreamHandler")
def test_setup_logger_adds_stream_handler_only(mock_stream_handler):
    """Tests that setup_logger adds only a StreamHandler if file_name is not specified."""
    logger_name = "stream_only"
    level = logging.INFO
    instance = mock_stream_handler.return_value
    logger = setup_logger(logger_name=logger_name, level=level)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], MagicMock)
    mock_stream_handler.assert_called_once_with(stream=sys.stdout)
    instance.setFormatter.assert_called_once()
    assert not any(isinstance(h, logging.FileHandler) for h in logger.handlers)


@patch("logging.StreamHandler")
@patch("logging.FileHandler")
def test_setup_logger_adds_stream_and_file_handler(
    mock_file_handler, mock_stream_handler
):
    """Tests that setup_logger adds a StreamHandler and FileHandler if file_name is specified."""
    logger_name = "stream_and_file"
    level = logging.WARNING
    file_name = "test.log"
    stream_instance = mock_stream_handler.return_value
    file_instance = mock_file_handler.return_value
    logger = setup_logger(logger_name=logger_name, level=level, file_name=file_name)
    assert len(logger.handlers) == 2
    stream_instance.setFormatter.assert_called_once()
    file_instance.setFormatter.assert_called_once()
    mock_file_handler.assert_called_once_with(filename=file_name)


def test_setup_logger_clears_existing_handlers():
    """Tests that setup_logger clears existing handlers before adding new ones. This ensures
    that the logger does not accumulate duplicate handlers over calls."""
    logger_name = "clear_handlers"
    level = logging.ERROR
    logger = logging.getLogger(logger_name)
    dummy_handler = logging.StreamHandler()
    logger.addHandler(dummy_handler)
    assert len(logger.handlers) == 1
    setup_logger(logger_name=logger_name, level=level)
    assert len(logger.handlers) == 1
    assert logger.handlers[0] is not dummy_handler


def test_setup_logger_formatter_format(monkeypatch):
    """Tests that the logger's formatter is set correctly and outputs the expected format."""
    logger_name = "formatter_test"
    level = logging.INFO
    log_msg = "Hello, logger!"
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stream)
    logger = setup_logger(logger_name=logger_name, level=level)
    logger.info(log_msg)
    output = stream.getvalue()
    assert logger_name in output
    assert "INFO" in output
    assert log_msg in output
