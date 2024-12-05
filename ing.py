from bank_base import BankBase
from file_manager import FileManager


class ING(BankBase):
    """
    ING-specific implementation of the BankBase class.

    This class provides functionality tailored to ING bank data, such as adjusting
    the 'Amount' column to properly reflect debits and credits.
    """

    def __init__(self, file_manager: FileManager, seperator: str = ';', decimal: str = ',',
                 encoding: str = 'utf-8', engine: str = 'openpyxl', header: int = 0):
        """
        Initialize the ING class with specific column indexes and defaults.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ';'.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
            header (int): Row index to use as column names. Default is 0.
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine, header)

        # Define column indexes specific to ING bank data
        self.date = 0
        self.iban = 3
        self.name = 1
        self.amount = 6
        self.amount_type = 5
        self.description = 8

    def load_file(self, file_path: str):
        """
        Load a CSV file into a pandas DataFrame.

        Parameters:
            file_path (str): Path to the input CSV file.

        Inherits error handling from the parent `load_file` method.
        """
        super().load_file(file_path)

    def edit_amount(self):
        """
        Adjust the 'Amount' column values to account for debit and credit transactions.

        This method ensures that debit amounts are negative and credit amounts are positive,
        based on the 'Debit/Credit' column in the ING dataset.

        Raises:
            IndexError: If the specified column indexes are out of range.
            Exception: For any other unexpected error during processing.
        """
        try:
            # Remove rows where all values are NaN
            self.df.dropna(how='all', inplace=True)

            # Validate column indexes
            if self.amount >= self.df.shape[1] or self.amount_type >= self.df.shape[1]:
                raise IndexError("Amount or Amount Type column index is out of range.")

            # Update 'Amount' values based on the transaction type
            self.df.iloc[:, self.amount] = self.df.apply(
                lambda row: -abs(row[self.amount]) if row[self.amount_type] == "Debit"
                else abs(row[self.amount]),
                axis=1
            )
        except Exception as e:
            print(f"An error occurred while editing amounts: {e}")

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int,
                     amount: int, description: int, iban: int):
        """
        Convert ING bank CSV data to an Excel file with transaction and income-expense sheets.

        Parameters:
            import_path (str): Path to the input CSV file.
            transactions_path (str): Path to save the output Excel file.
            date (int): Column index for the date.
            name (int): Column index for the transaction name.
            amount (int): Column index for the transaction amount.
            description (int): Column index for the transaction description.
            iban (int): Column index for the IBAN.

        Inherits error handling and functionality from the parent `csv_to_excel` method.
        """
        self.edit_amount()
        return super().csv_to_excel(
            import_path,
            transactions_path,
            self.date,
            self.name,
            self.amount,
            self.description,
            self.iban
        )
