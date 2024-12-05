# Bank Transactions Processor
A Python application to process bank transactions from CSV files and convert them into Excel files. The Excel files contain two sheets. The first sheet shows the transactions and the second sheet shows an income-expense table. This project supports transactions from **SNS Bank**, **RABO Bank**, and **ING Bank**.

---

## Features
- Converts CSV transaction data to Excel format.
- Automatically organizes output files into the correct directory.
- Provides bank-specific processing for SNS, RABO, and ING banks.

---

## Prerequisites
Before using the application, ensure you have the following:
- Python 3.7 or higher installed.
- Required dependencies installed. Run:

  ```bash
  pip install -r requirements.txt
  ```

## Directory Structure
The application expects the following folder structure for input files:
```
project_root/
├── data/
│   ├── sns/
│   │   └── 2024/
│   │       ├── january.csv
│   │       ├── february.csv
│   │       └── etc.
│   ├── rabo/
│   │   └── 2024/
│   │       ├── january.csv
│   │       ├── february.csv
│   │       └── etc.
│   └── ing/
│       └── 2024/
│           ├── january.csv
│           ├── february.csv
│           └── etc.
├── results/
│   ├── sns/
│   ├── rabo/
│   └── ing/
├── bank_base.py
├── file_manager.py
├── ing.py
├── LICENSE.md
├── main.py
├── rabo.py
├── README.md
├── requirements.txt
└── sns.py
```
- `data/`: Contains the input CSV files.
    - Each bank has its subfolder (`sns`, `rabo`, `ing`).
    - Each bank subfolder has a year folder (e.g., `2024`).
    - CSV files are named by month (e.g., `january.csv`, `february.csv`).
- `results/`: The folder where processed Excel files are saved. The folder structure matches the input (`bank_name/year/`). This folder is automatically created if the csv file is successfully converted to excel.

## How to Use
1. Prepare Input Files
- Place your CSV files in the `data` folder under the correct bank, year, and file name (e.g., `data/sns/2024/january.csv`).
2. Run the Application
- Open a terminal in the project directory and run:
```bash
python main.py
```
3. Follow the Prompts
- Enter the year (e.g., `2024`).
- Enter the month (e.g., `january` or `february`).
- Choose the bank:
    - `1` for SNS Bank
    - `2` for RABO Bank
    - `3` for ING Bank
4. Find the Output
- The processed Excel file will be saved in the `results` folder under the corresponding bank and year.

## Example
### Input
- A CSV file located at data/sns/2024/january.csv.
### Steps
1. Run the application.
2. Input:
```
Enter the year: 2024
Enter the month: january
Choose one of the following banks:
1. SNS Bank
2. RABO Bank
3. ING Bank
I choose option (type in a number): 1
```
3. The application processes the file and saves the output to `results/sns/2024/january.xlsx`.

## Requirements
- Python Modules:
    - `pandas`
    - `openpyxl`
    - Other dependencies listed in `requirements.txt`.

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Error Handling
- If an input file is missing or improperly named, the application will raise a `FileNotFoundError`.
- If incorrect input is provided (e.g., invalid year or bank option), the application will prompt you to correct it.

## Customization
- Update bank-specific processing rules by modifying the respective classes (`SNS`, `RABO`, `ING`) in their respective files (`sns.py`, `rabo.py`, `ing.py`).
- Change the directory structure or default paths by modifying the `FileManager` class in `file_manager.py`.

## Notes
- Ensure that input CSV files use the expected format specific to each bank.
- The application does not validate CSV file contents; incorrect formatting may lead to errors during processing.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
