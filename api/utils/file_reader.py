import logging

from pypdf import PdfReader

from api.utils.setup_logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)


def read_file(file_path: str) -> str:
    """
    Reads an input file and returns its text content. Supported file formats
        include PDF and CSV.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The text content of the file.
    """
    if file_path.lower().endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            logger.info(f"Total pages: {len(reader.pages)}")
            output_content = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                output_content += f"--- Page {i + 1} ---\n"
                output_content += text if text else "[No extractable text]\n"
            return output_content
        except Exception as e:
            logger.error(f"Failed to read PDF file {file_path}: {e}")
            raise RuntimeError(f"Failed to read PDF file: {e}")
    elif file_path.lower().endswith(".csv"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            logger.info(f"Read CSV file {file_path} successfully.")
            return content
        except Exception as e:
            logger.error(f"Failed to read CSV file {file_path}: {e}")
            raise RuntimeError(f"Failed to read CSV file: {e}")
    else:
        logger.error(
            f"Unsupported file format for file {file_path}. Supported formats are PDF and CSV."
        )
        raise ValueError("Unsupported file format. Please provide a PDF or CSV file.")
