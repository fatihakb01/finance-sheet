# Import module
from file_manager import FileManager


class BankBase:
    def __init__(self, file_manager: FileManager, seperator: str = ';', decimal: str = ',',
                 encoding: str = 'utf-8', engine: str = 'openpyxl'):
        """
        Initialize the base class with shared properties.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ';'.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
        """
        self.file_manager = file_manager
        self.df = None
        self.seperator = seperator
        self.decimal = decimal
        self.encoding = encoding
        self.engine = engine
