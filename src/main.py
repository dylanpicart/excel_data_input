import os
import logging
import pandas as pd
from utils import setup_logging, convert_path_if_wsl, load_excel, normalize_columns, ensure_output_directory, validate_input_file
from synonym_map import BASE_PRIMARY_KEY, ALL_SYNONYM_MAPS

setup_logging()

def merge_sheets(sheet1, sheet2, map_key="ethnicity"):
    """Merge data from two Excel sheets based on synonym mappings."""
    synonym_map = ALL_SYNONYM_MAPS[map_key]
    base_key = BASE_PRIMARY_KEY.lower().strip()  # Normalize base key

    # Normalize primary key map
    primary_key_map = {k.lower().strip(): [i.lower().strip() for i in v] for k, v in ALL_SYNONYM_MAPS["primary_key"].items()}

    normalize_columns(sheet1)
    normalize_columns(sheet2)

    for col in sheet2.columns:
        if col in primary_key_map[base_key]:  # Use primary_key_map here
            sheet2.rename(columns={col: base_key}, inplace=True)
            break

    sheet1[base_key] = sheet1[base_key].astype(str).str.lower().str.strip()
    sheet2[base_key] = sheet2[base_key].astype(str).str.lower().str.strip()

    merged_df = sheet1.copy()
    sheet2_columns = sheet2.columns.str.lower()

    for column in sheet1.columns:
        if column == base_key:
            continue
        key = column.replace("(count)", "").replace("(percent)", "").strip().lower()
        synonyms = synonym_map.get(key, [key])
        matched_col = next((col for col in sheet2_columns if any(syn in col for syn in synonyms)), None)

        if matched_col:
            merged_df[column] = merged_df[base_key].map(sheet2.set_index(base_key)[matched_col])
        else:
            logging.warning(f"No match found for column '{column}'. Retaining original values.")

    merged_df.columns = merged_df.columns.str.lower().str.strip()
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated(keep='first')]
    logging.info("Data merge completed successfully.")
    return merged_df


def main(file_path, output_dir="data/output", map_key="ethnicity"):
    """Main function to load Excel sheets, merge data, and save output."""
    file_path = os.path.normpath(convert_path_if_wsl(file_path.strip('"')))
    validate_input_file(file_path)  # Validate input file before proceeding
    output_dir = ensure_output_directory(os.path.normpath(convert_path_if_wsl(output_dir.strip('"'))))

    excel_file = load_excel(file_path)
    if "Sheet1" not in excel_file.sheet_names or "Sheet2" not in excel_file.sheet_names:
        raise ValueError("Both 'Sheet1' and 'Sheet2' must be present in the Excel file.")

    sheet1 = excel_file.parse("Sheet1")
    sheet2 = excel_file.parse("Sheet2")

    merged_df = merge_sheets(sheet1, sheet2, map_key)
    output_filename = f"merged_{os.path.basename(file_path)}"
    output_path = os.path.join(output_dir, output_filename)
    merged_df.to_excel(output_path, index=False)
    logging.info(f"Merged file saved to: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge Excel sheets with column mapping.")
    parser.add_argument("--file_path", required=True, help="Path to the input Excel file.")
    parser.add_argument("--output_dir", default="data/output", help="Directory to save the output file.")
    parser.add_argument("--map_key", choices=ALL_SYNONYM_MAPS.keys(), default="ethnicity", help="Mapping type.")
    args = parser.parse_args()
    main(file_path=args.file_path, output_dir=args.output_dir, map_key=args.map_key)
