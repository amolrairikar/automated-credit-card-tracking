import pytest
from unittest.mock import patch
from api.utils.file_reader import read_csv_file
from unittest.mock import mock_open


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2\nval1,val2\n")
@patch("api.utils.file_reader.logger")
def test_read_csv_success(mock_logger, _):
    result = read_csv_file(file_path="file.csv")
    assert "col1,col2" in result
    assert "val1,val2" in result
    mock_logger.info.assert_called_with("Read CSV file file.csv successfully.")


@patch("builtins.open", side_effect=FileNotFoundError("Did not find CSV file"))
@patch("api.utils.file_reader.logger")
def test_read_csv_file_not_found_exception(mock_logger, _):
    with pytest.raises(FileNotFoundError) as excinfo:
        read_csv_file(file_path="file.csv")
    assert "Did not find CSV file" in str(excinfo.value)
    mock_logger.error.assert_called()


@patch("builtins.open", side_effect=PermissionError("Permission denied for CSV file"))
@patch("api.utils.file_reader.logger")
def test_read_csv__permissionexception(mock_logger, _):
    with pytest.raises(PermissionError) as excinfo:
        read_csv_file(file_path="file.csv")
    assert "Permission denied for CSV file" in str(excinfo.value)
    mock_logger.error.assert_called()


@patch(
    "builtins.open",
    side_effect=UnicodeDecodeError(
        "utf-8", b"bad", 0, 1, "CSV file is not UTF-8 encoded"
    ),
)
@patch("api.utils.file_reader.logger")
def test_read_csv_unicode_decode_exception(mock_logger, _):
    with pytest.raises(UnicodeDecodeError):
        read_csv_file(file_path="file.csv")
    mock_logger.error.assert_called()
