from api.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def read_csv_file(file_path: str) -> str:
    """
    Reads an input CSV file and returns its content as a string.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        str: The text content of the CSV file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        logger.info(f"Read CSV file {file_path} successfully.")
        return content
    except FileNotFoundError as e:
        logger.error("Did not find CSV file at path: %s", file_path)
        raise FileNotFoundError(str(e))
    except PermissionError as e:
        logger.error("Permission denied for CSV file at path: %s", file_path)
        raise PermissionError(str(e))
    except UnicodeDecodeError:
        logger.error("CSV file is not UTF-8 encoded")
        raise
