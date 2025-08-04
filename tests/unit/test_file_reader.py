import pytest
from unittest.mock import patch
from api.utils.file_reader import read_file
from unittest.mock import mock_open


@pytest.fixture
def mock_pdf_reader():
    class MockPage:
        def __init__(self, text):
            self._text = text

        def extract_text(self):
            return self._text

    class MockPdfReader:
        def __init__(self, pages):
            self.pages = pages

    return MockPage, MockPdfReader


@patch("api.utils.file_reader.PdfReader")
@patch("api.utils.file_reader.logger")
def test_read_pdf_single_page(mock_logger, mock_pdf_reader_class, mock_pdf_reader):
    MockPage, MockPdfReader = mock_pdf_reader
    mock_pdf_reader_class.return_value = MockPdfReader([MockPage("Hello World")])
    result = read_file("dummy.pdf")
    assert "--- Page 1 ---" in result
    assert "Hello World" in result
    mock_logger.info.assert_called_with("Total pages: 1")


@patch("api.utils.file_reader.PdfReader")
@patch("api.utils.file_reader.logger")
def test_read_pdf_multiple_pages(mock_logger, mock_pdf_reader_class, mock_pdf_reader):
    MockPage, MockPdfReader = mock_pdf_reader
    mock_pdf_reader_class.return_value = MockPdfReader(
        [
            MockPage("Page 1 text"),
            MockPage("Page 2 text"),
            MockPage("Page 3 text"),
        ]
    )
    result = read_file("dummy.pdf")
    assert "--- Page 1 ---" in result
    assert "--- Page 2 ---" in result
    assert "--- Page 3 ---" in result
    assert "Page 1 text" in result
    assert "Page 2 text" in result
    assert "Page 3 text" in result
    mock_logger.info.assert_called_with("Total pages: 3")


@patch("api.utils.file_reader.PdfReader")
@patch("api.utils.file_reader.logger")
def test_read_pdf_page_with_no_text(
    mock_logger, mock_pdf_reader_class, mock_pdf_reader
):
    MockPage, MockPdfReader = mock_pdf_reader
    mock_pdf_reader_class.return_value = MockPdfReader(
        [
            MockPage(None),
            MockPage("Some text"),
        ]
    )
    result = read_file("dummy.pdf")
    assert "--- Page 1 ---" in result
    assert "[No extractable text]" in result
    assert "--- Page 2 ---" in result
    assert "Some text" in result
    mock_logger.info.assert_called_with("Total pages: 2")


@patch("api.utils.file_reader.PdfReader")
@patch("api.utils.file_reader.logger")
def test_read_pdf_empty_pdf(mock_logger, mock_pdf_reader_class, mock_pdf_reader):
    _, MockPdfReader = mock_pdf_reader
    mock_pdf_reader_class.return_value = MockPdfReader([])
    result = read_file("dummy.pdf")
    assert result == ""
    mock_logger.info.assert_called_with("Total pages: 0")


@patch("api.utils.file_reader.PdfReader")
def test_read_pdf_exception(mock_pdf_reader_class, mock_pdf_reader):
    _, _ = mock_pdf_reader
    mock_pdf_reader_class.return_value = Exception("PDF error")
    with pytest.raises(RuntimeError) as excinfo:
        read_file("dummy.pdf")
    assert "Failed to read PDF file" in str(excinfo.value)


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2\nval1,val2\n")
@patch("api.utils.file_reader.logger")
def test_read_csv_success(mock_logger, _):
    result = read_file("file.csv")
    assert "col1,col2" in result
    assert "val1,val2" in result
    mock_logger.info.assert_called_with("Read CSV file file.csv successfully.")


@patch("builtins.open", side_effect=Exception("CSV error"))
@patch("api.utils.file_reader.logger")
def test_read_csv_exception(mock_logger, _):
    with pytest.raises(RuntimeError) as excinfo:
        read_file("file.csv")
    assert "Failed to read CSV file" in str(excinfo.value)
    mock_logger.error.assert_called()


@patch("api.utils.file_reader.logger")
def test_read_file_unsupported_format(mock_logger):
    with pytest.raises(ValueError) as excinfo:
        read_file("file.txt")
    assert "Unsupported file format" in str(excinfo.value)
    mock_logger.error.assert_called()
