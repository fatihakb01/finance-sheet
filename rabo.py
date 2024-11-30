# Import modules
import pandas as pd
from bank_base import BankBase
from file_manager import FileManager


class RABO(BankBase):
    def __init__(self, file_manager, seperator: str = ',', decimal: str = ',', encoding: str = 'ANSI',
                 engine: str = 'openpyxl'):
        """
        Initialize the RABO class with specific defaults or custom arguments.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ','.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
        """
        super().__init__(file_manager, seperator, decimal, encoding, engine)
        self.column_names = ['DateOfTransaction', 'IBAN', 'Name', 'Amount', 'Description']
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

        Raises:
            FileNotFoundError: If the specified file path does not exist.
            ValueError: If the file content is invalid or unreadable.
            Exception: For any other unexpected error.
        """
        self.df = None
        try:
            # Attempt to load the CSV file
            self.df = pd.read_csv(
                file_path,
                sep=self.seperator,
                decimal=self.decimal,
                encoding=self.encoding,
                header=0
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except ValueError as e:
            raise ValueError(f"Invalid file: {file_path}") from e
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}") from e

    def create_transactions_sheet(self) -> pd.DataFrame:
        """
        Create a DataFrame for transactions data.
        Returns:
            pd.DataFrame: DataFrame containing the transactions.
        """
        try:
            # # Ensure names are assigned before saving to Excel
            # self.assign_names()

            # Select the specified columns by their index
            column_idx = [self.date, self.iban, self.name, self.amount, self.description]
            filtered_df = self.df.iloc[:, column_idx]

            # Rename the columns for better readability in the Excel file
            filtered_df.columns = self.column_names

            return filtered_df
        except Exception as e:
            print(f"Error creating income-expense sheet: {e}")
            return pd.DataFrame()

    def csv_to_excel(self, import_path: str, transactions_path: str):
        """
        Convert a CSV file to an Excel file with specific columns.

        The method selects specific columns from the DataFrame, assigns meaningful
        column names, and saves the resulting data to an Excel file.

        Parameters:
            import_path (str): Path to the input CSV file.
            transactions_path (str): Path to save the output Excel file.

        Raises:
            IndexError: If column indexes are out of range.
            Exception: For any other unexpected error during conversion.
        """
        try:
            # Generate the transactions table
            filtered_df = self.create_transactions_sheet()

            # Save both sheets to the Excel file
            with pd.ExcelWriter(f"{transactions_path}.xlsx", engine=self.engine) as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Transactions')

            print(f"Successfully converted '{import_path}' to '{transactions_path}.xlsx' with selected columns.")
        except IndexError as e:
            print(f"Column index out of range: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
