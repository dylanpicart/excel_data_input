# Excel Merger Project

This project provides a Python tool to merge Excel sheets dynamically, handling variations in column names using synonym maps.

## Project Structure
```
project-root/
│
├── data/                         # Contains input and output Excel files
│   ├── input/                    # Input Excel files (Useful for testing)
│   └── output/                   # Output merged Excel files
│
├── logs/                         # Contains log files
│
├── src/                          # Source code directory
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # Main script for merging
│   ├── utils.py                  # Utility functions
│   └── synonym_map.py            # Synonym mappings - open to being updated
│
├── venv/                         # Virtual environment directory
│
├── .gitignore                    # Git ignore file
│
├── tests/                        # Contains test scripts
│
├── requirements.txt              # Project dependencies
├── setup.py                      # Setup script for packaging
├── LICENSE                       # License file for the project
└── README.md                     # Project documentation
```

## Requirements
- Python 3.7+
- `pandas`, `openpyxl`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Setup and Installation
To package the project, run:
```bash
python setup.py sdist
```
Install the package with:
```bash
pip install dist/excel_merger-1.0.0.tar.gz
```

## Running the Script

### **Bash (WSL/Linux)**:
**Add Function to .bashrc:**
```bash
echo 'excelmerge() { /mnt/c/path/to/venv/bin/python3 /mnt/c/path/to/src/main.py "$@"; }' >> ~/.bashrc
source ~/.bashrc
```
Then run:
```bash
excelmerge --file_path "/mnt/c/path/to/input.xlsx" --map_key ethnicity
```

### **PowerShell (Windows)**:
**Add Function to PowerShell Profile:**
```powershell
notepad $PROFILE
```
Add the following line:
```powershell
function excelmerge { C:\path\to\venv\Scripts\python.exe "C:\path\to\src\main.py" @args }
```
Then run:
```powershell
. $PROFILE
excelmerge --file_path "C:\path\to\input.xlsx" --map_key ethnicity
```

---

## Setup Details for Windows and Bash
- **Windows**: Ensure Python is added to the PATH.
- **Bash (WSL)**: Install Python using `sudo apt install python3`.
- **Fix for os.uname()**: Use `platform.release()` in `utils.py`.


## Usage
After installation, run the tool from any terminal:
```bash
excelmerge --file_path "path_to_excel_file.xlsx" --map_key ethnicity
```

## How to Use
1. Place your input Excel file in `data/input/`.
2. Run the script via terminal.
3. The merged Excel will appear in `data/output/`.

Once the script completes, you can open the merged Excel file directly using:

**Bash (WSL/Linux)**:
```bash
xdg-open data/output/merged_input.xlsx
```

**PowerShell (Windows)**:
```powershell
Start-Process "data/output/merged_input.xlsx"
```

**Note:** You can also run the script from any directory if you have added the alias or function as instructed.

## What is Required
- Excel sheets must have consistent structure.
- Sheets must be named `Sheet1` and `Sheet2`.
- Primary Key currently must be `DBN`.
- Ensure your `path/to/excel_file.xlsx` does not contain spaces.

## Contribution
Feel free to fork this project, submit issues, and contribute through pull requests! Contributions to `synonym_map.py` are most welcome.

## Automating Tests with Pytest

To ensure reliable testing, consider these steps:

- **pytest.ini**: Sets pytest paths and options.
- **conftest.py**: Adds project paths automatically.
- **pre-commit**: Runs tests before commits.
- **Makefile**: Simplifies running test commands.
- **IDE Integration**: Runs tests as you code.
- **tox**: Tests across Python versions.

While optional for smaller projects, these steps enhance test reliability and automation.

**Note**: For testing, run the following if `pytest tests/` returns a `ModuleNotFoundError`:
```bash
venv/bin/python -m pytest tests/
```
## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Author**
Developed by **Dylan Picart at Partnership With Children**.

For questions or contributions, contact: [dpicart@partnershipwithchildren.org](mailto:dpicart@partnershipwithchildren.org).
