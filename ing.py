# Import modules
from bank_base import BankBase
from file_manager import FileManager


class ING(BankBase):
    def __init__(self, file_manager, seperator: str = ';', decimal: str = ',', encoding: str = 'utf-8',
                 engine: str = 'openpyxl', header: int = 0):
        """
        Initialize the ING class with specific defaults or custom arguments.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ','.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine, header)
        self.date = 0
        self.iban = 3
        self.name = 1
        self.amount = 6
        self.amount_type = 5
        self.description = 8

    def load_file(self, file_path: str):
        super().load_file(file_path)

    def edit_amount(self):
        """
        Adjust the amounts in the loaded data to reflect debits as negative values.

        Modifies the 'Amount (EUR)' column to have negative values for 'Debit' transactions
        and positive values for 'Credit' transactions.
        """
        try:
            # Delete empty rows
            self.df.dropna(how='all', inplace=True)

            # Check if required column indexes are valid
            if self.amount >= self.df.shape[1] or self.amount_type >= self.df.shape[1]:
                raise IndexError("Amount or Amount Type column index is out of range.")

            # Convert the 'Amount' column values based on the 'Debit/Credit' column
            self.df.iloc[:, self.amount] = self.df.apply(
                lambda row: -abs(row[self.amount]) if row[self.amount_type] == "Debit" else abs(row[self.amount]),
                axis=1
            )
        except Exception as e:
            print(f"An error occurred while editing amounts: {e}")

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int, amount: int,
                     description: int, iban: int):
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
