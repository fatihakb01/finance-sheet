import pandas as pd
from bank_base import BankBase


class SNS(BankBase):
    """
    SNS-specific implementation of the BankBase class.

    This class handles CSV files from SNS Bank, allowing data to be processed
    and converted into a standardized Excel format with transaction details.
    """

    def __init__(self, file_manager, seperator: str = ';', decimal: str = ',', encoding: str = 'utf-8',
                 engine: str = 'openpyxl', header: int = None):
        """
        Initialize the SNS class with specific column mappings and defaults.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ';'.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
            header (int): Row index to use as column names. Default is None (no headers).
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine, header)

        # Define column indexes specific to SNS Bank data
        self.date = 0
        self.iban = 2
        self.name = 3
        self.amount = 10
        self.description = 17

    def load_file(self, file_path: str):
        """
        Load a CSV file into a pandas DataFrame.

        Parameters:
            file_path (str): Path to the input CSV file.

        Inherits functionality from the parent `load_file` method, including error handling.
        """
        super().load_file(file_path)

    def assign_names(self):
        """
        Assign names to transactions with missing or empty names.

        This method ensures all transactions have a name. If the 'Name' column is missing
        or empty, the first word from the 'Description' column is used. If the 'Description'
        column is also missing, a default value of 'Unknown' is assigned.

        Raises:
            IndexError: If the required column indexes for 'Name' or 'Description'
                        are out of the DataFrame's range.
            Exception: For any other unexpected errors during assignment.
        """
        try:
            # Check if the column indexes are within the DataFrame's range
            if self.name >= self.df.shape[1] or self.description >= self.df.shape[1]:
                raise IndexError("Name or Description column index is out of range.")

            # Fill missing 'Name' values using the first part of the 'Description' column
            self.df.iloc[:, self.name] = self.df.iloc[:, self.name].fillna(
                self.df.iloc[:, self.description].apply(
                    lambda x: str(x).split(">")[0] if pd.notnull(x) else "Unknown"
                )
            )
        except Exception as e:
            print(f"An error occurred while assigning names: {e}")

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int,
                     amount: int, description: int, iban: int):
        """
        Convert SNS Bank CSV data to an Excel file with transaction and income-expense sheets.

        This method first ensures all transactions have assigned names and then converts
        the CSV data into a structured Excel format.

        Parameters:
            import_path (str): Path to the input CSV file.
            transactions_path (str): Path to save the output Excel file.
            date (int): Column index for the date.
            name (int): Column index for the transaction name.
            amount (int): Column index for the transaction amount.
            description (int): Column index for the transaction description.
            iban (int): Column index for the IBAN.

        Returns:
            str: Path to the generated Excel file.

        Inherits functionality from the parent `csv_to_excel` method.
        """
        # Ensure names are assigned before converting to Excel
        self.assign_names()
        return super().csv_to_excel(
            import_path,
            transactions_path,
            self.date,
            self.name,
            self.amount,
            self.description,
            self.iban
        )
