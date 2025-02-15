import pytest
import pandas as pd
import os
from src.main import main
from src.synonym_map import ALL_SYNONYM_MAPS, BASE_PRIMARY_KEY

def test_main_success(tmp_path):
    # Create sample Excel files
    input_file = tmp_path / "input.xlsx"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    df1 = pd.DataFrame({"DBN": [1, 2], "Latino/Hispanic (count)": [None, None]})
    df2 = pd.DataFrame({"Code #": [1, 2], "# Latino": [10, 20]})
    with pd.ExcelWriter(input_file) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)

    main(str(input_file), str(output_dir), map_key="ethnicity")

    output_files = list(output_dir.glob("*.xlsx"))
    assert len(output_files) == 1

    merged_df = pd.read_excel(output_files[0])
    assert "latino/hispanic (count)" in merged_df.columns
    assert list(merged_df["latino/hispanic (count)"]) == [10, 20]

def test_main_invalid_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        main("non_existent.xlsx", str(tmp_path))

def test_main_invalid_format(tmp_path):
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("Invalid content")
    with pytest.raises(ValueError):
        main(str(invalid_file), str(tmp_path))
