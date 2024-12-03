# Import modules
import pandas as pd
from bank_base import BankBase


class SNS(BankBase):
    def __init__(self, file_manager, seperator: str = ';', decimal: str = ',', encoding: str = 'utf-8',
                 engine: str = 'openpyxl', header: int = None):
        """
        Initialize the RABO class with specific defaults or custom arguments.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ','.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine, header)
        self.date = 0
        self.iban = 2
        self.name = 3
        self.amount = 10
        self.description = 17

    def load_file(self, file_path: str):
        super().load_file(file_path)

    def assign_names(self):
        """
        Assign names to transactions with missing or empty names.

        Missing names are replaced with the first word from the 'Description' column.
        If the 'Description' column is also missing, a default value 'Unknown' is assigned.

        Raises:
            IndexError: If the required column indexes are out of range.
            Exception: For any other unexpected error during assignment.
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

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int, amount: int,
                     description: int, iban: int):
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
