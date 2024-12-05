from bank_base import BankBase
from file_manager import FileManager


class RABO(BankBase):
    """
    RABO-specific implementation of the BankBase class.

    This class is designed to handle Rabobank CSV files and convert them into a
    standardized Excel format with transaction details.
    """

    def __init__(self, file_manager: FileManager, seperator: str = ',', decimal: str = ',',
                 encoding: str = 'ANSI', engine: str = 'openpyxl', header: int = 0):
        """
        Initialize the RABO class with specific column mappings and defaults.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ','.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'ANSI'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
            header (int): Row index to use as column names. Default is 0.
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine, header)

        # Define column indexes specific to Rabobank data
        self.date = 4
        self.iban = 8
        self.name = 9
        self.amount = 6
        self.description = 19

    def load_file(self, file_path: str):
        """
        Load a CSV file into a pandas DataFrame.

        Parameters:
            file_path (str): Path to the input CSV file.

        Inherits functionality from the parent `load_file` method, including error handling.
        """
        super().load_file(file_path)

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int,
                     amount: int, description: int, iban: int):
        """
        Convert Rabobank CSV data to an Excel file with transaction and income-expense sheets.

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

        Inherits error handling and functionality from the parent `csv_to_excel` method.
        """
        return super().csv_to_excel(
            import_path,
            transactions_path,
            self.date,
            self.name,
            self.amount,
            self.description,
            self.iban
        )
