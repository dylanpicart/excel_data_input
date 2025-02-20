import os
import logging
import platform
import pandas as pd

def setup_logging():
    """Set up logging configuration for the project.

    Logs are saved in the 'logs' directory, creating the directory if necessary.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "merger.log"), mode='w'),
            logging.StreamHandler()
        ]
    )

def validate_input_file(file_path):
    """Validate that the input file exists and is an Excel file.

    Args:
        file_path (str): Path to the input file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not an Excel file.
    """
    if not file_path.endswith(('.xlsx', '.xls', '.xlsb', '.xlsm', '.csv')):
        raise ValueError("Invalid file format. Please provide an Excel file.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
        

def convert_path_if_wsl(path):
    """Convert Windows path to WSL path if running in WSL.

    Args:
        path (str): Path to be converted.

    Returns:
        str: Converted path for WSL or original path.
    """
    if 'microsoft' in platform.release().lower():
        return path.replace("\\", "/").replace("C:/", "/mnt/c/")
    return path

def load_excel(file_path):
    """Load an Excel file and return an ExcelFile object.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.ExcelFile: Loaded Excel file object.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file is not a valid Excel file.
    """
    try:
        return pd.ExcelFile(file_path)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise

def normalize_columns(df):
    """Normalize column names by stripping whitespace and converting to lowercase.

    Args:
        df (pd.DataFrame): DataFrame whose columns need to be normalized.
    """
    df.columns = df.columns.str.lower().str.strip()

def ensure_output_directory(output_dir):
    """Ensure that the output directory exists, creating it if necessary.

    Args:
        output_dir (str): Path to the output directory.

    Returns:
        str: The path to the output directory.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, output_dir)
    os.makedirs(output_path, exist_ok=True)
    return output_path
