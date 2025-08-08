import logging
import sys


def setup_logger(
    logger_name: str, level: int = logging.INFO, file_name=None
) -> logging.Logger:
    """
    Sets up a logger for the application with a given name and logging level. Optionally logs to
    a file specified by file_name.

    Args:
        logger_name (str): The name of the logger.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
        file_name (str): An optional file path. If provided, logs will be written to this file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(level=level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)
    if file_name:
        fh = logging.FileHandler(filename=file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
