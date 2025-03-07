import pytest
import os
import pandas as pd
from src.utils import validate_input_file, convert_path_if_wsl, load_excel, normalize_columns, ensure_output_directory

def test_validate_input_file(tmp_path):
    valid_file = tmp_path / "test.xlsx"
    valid_file.touch()
    with pytest.raises(FileNotFoundError):
        validate_input_file("non_existent.xlsx")
    with pytest.raises(ValueError):
        validate_input_file("invalid.txt")
    assert validate_input_file(str(valid_file)) is None

def test_convert_path_if_wsl():
    path = "C:\\Users\\test\\file.xlsx"
    result = convert_path_if_wsl(path)
    assert result == path or result.startswith("/mnt/")

def test_load_excel(tmp_path):
    file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"col": [1, 2]})
    df.to_excel(file, index=False)
    excel_file = load_excel(str(file))
    assert isinstance(excel_file, pd.ExcelFile)

def test_normalize_columns():
    df = pd.DataFrame(columns=[" Col1 ", "COL2", "col3"])
    normalize_columns(df)
    assert all(col in df.columns for col in ["col1", "col2", "col3"])

def test_ensure_output_directory(tmp_path):
    path = tmp_path / "new_output"
    result = ensure_output_directory(str(path))
    assert os.path.exists(result)
