# Import modules
from bank_base import BankBase
from file_manager import FileManager


class RABO(BankBase):
    def __init__(self, file_manager, seperator: str = ',', decimal: str = ',', encoding: str = 'ANSI',
                 engine: str = 'openpyxl', header: int = 0):
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
        self.date = 4
        self.iban = 8
        self.name = 9
        self.amount = 6
        self.description = 19

    def load_file(self, file_path: str):
        super().load_file(file_path)

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int, amount: int,
                     description: int, iban: int):
        return super().csv_to_excel(
            import_path,
            transactions_path,
            self.date,
            self.name, self.amount,
            self.description,
            self.iban
        )
