from file_manager import FileManager
import pandas as pd


class BankBase:
    """
    A base class for managing bank transactions and creating income-expense reports.

    Attributes:
        file_manager (FileManager): Manages file paths and operations.
        seperator (str): Delimiter used in CSV files. Default is ';'.
        decimal (str): Decimal separator used in CSV files. Default is ','.
        encoding (str): Character encoding for file reading. Default is 'utf-8'.
        engine (str): Engine for Excel file operations. Default is 'openpyxl'.
        header (int): Row number to use as the column names. Default is None.
        df (pd.DataFrame): DataFrame to hold the loaded data.
        column_names (list): Standard column names for transactions.
    """

    def __init__(self, file_manager: FileManager, seperator: str = ';', decimal: str = ',',
                 encoding: str = 'utf-8', engine: str = 'openpyxl', header: int = None):
        self.df = None
        self.column_names = ['Date', 'IBAN', 'Name', 'Amount', 'Description']
        self.file_manager = file_manager
        self.seperator = seperator
        self.decimal = decimal
        self.encoding = encoding
        self.engine = engine
        self.header = header

    def load_file(self, file_path: str):
        """
        Load a CSV file into a DataFrame.

        Parameters:
            file_path (str): Path to the input CSV file.

        Raises:
            FileNotFoundError: If the file is not found.
            ValueError: If the file is empty or invalid.
            Exception: For unexpected errors.
        """
        try:
            self.df = pd.read_csv(
                file_path,
                sep=self.seperator,
                decimal=self.decimal,
                encoding=self.encoding,
                header=self.header
            )
            if self.df.empty:
                raise ValueError(f"The file at {file_path} is empty or invalid.")
        except (FileNotFoundError, ValueError, Exception) as e:
            raise e

    def assign_iban(self, iban: int):
        """
        Replace missing or empty IBAN values with 'Unknown IBAN'.

        Parameters:
            iban (int): Index of the IBAN column.
        """
        try:
            self.df.iloc[:, iban] = self.df.iloc[:, iban].apply(
                lambda x: 'Unknown IBAN' if not pd.notnull(x) or x == '' else x
            )
        except Exception as e:
            print(f"Error while assigning IBAN: {e}")

    def create_transactions_sheet(self, date: int, name: int, amount: int, description: int, iban: int) -> pd.DataFrame:
        """
        Create a DataFrame with standardized transaction details.

        Parameters:
            date (int): Index of the Date column.
            name (int): Index of the Name column.
            amount (int): Index of the Amount column.
            description (int): Index of the Description column.
            iban (int): Index of the IBAN column.

        Returns:
            pd.DataFrame: DataFrame containing transactions.
        """
        try:
            self.assign_iban(iban)
            column_idx = [date, iban, name, amount, description]
            filtered_df = self.df.iloc[:, column_idx]
            filtered_df.columns = self.column_names
            return filtered_df
        except Exception as e:
            print(f"Error creating transactions sheet: {e}")
            return pd.DataFrame()

    def create_income_expense_sheet(self, date: int, name: int, amount: int, description: int,
                                    iban: int) -> pd.DataFrame:
        """
        Create an income-expense table grouped by Name and IBAN.

        Parameters:
            date (int): Index of the Date column.
            name (int): Index of the Name column.
            amount (int): Index of the Amount column.
            description (int): Index of the Description column.
            iban (int): Index of the IBAN column.

        Returns:
            pd.DataFrame: DataFrame with income and expense details.
        """
        try:
            filtered_df = self.create_transactions_sheet(date, name, amount, description, iban)
            grouped = filtered_df.groupby(['Name', 'IBAN'])['Amount'].sum()

            income_df = grouped[grouped > 0].reset_index()
            income_df.columns = ['Income Names', 'IBAN', 'Income Amounts']

            expense_df = grouped[grouped < 0].reset_index()
            expense_df.columns = ['Expense Names', 'IBAN', 'Expense Amounts']

            max_length = max(len(income_df), len(expense_df))
            income_df = income_df.reindex(range(max_length)).fillna('')
            expense_df = expense_df.reindex(range(max_length)).fillna('')

            return pd.DataFrame({
                'Income Names': income_df['Income Names'],
                'Income Amounts': income_df['Income Amounts'],
                'Expense Names': expense_df['Expense Names'],
                'Expense Amounts': expense_df['Expense Amounts']
            })
        except Exception as e:
            print(f"Error creating income-expense sheet: {e}")
            return pd.DataFrame()

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int, amount: int,
                     description: int, iban: int):
        """
        Convert a CSV file to an Excel file with transactions and income-expense sheets.

        Parameters:
            import_path (str): Path to the input CSV file.
            transactions_path (str): Path to save the output Excel file.
            date (int): Index of the Date column.
            name (int): Index of the Name column.
            amount (int): Index of the Amount column.
            description (int): Index of the Description column.
            iban (int): Index of the IBAN column.

        Raises:
            IndexError: If column indexes are invalid.
            Exception: For unexpected errors during the conversion.
        """
        try:
            filtered_df = self.create_transactions_sheet(date, name, amount, description, iban)
            income_expense_df = self.create_income_expense_sheet(date, name, amount, description, iban)

            with pd.ExcelWriter(f"{transactions_path}.xlsx", engine=self.engine) as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Transactions')
                income_expense_df.to_excel(writer, index=False, sheet_name='Income & Expenses')

            print(f"Successfully converted '{import_path}' to '{transactions_path}.xlsx'.")
        except (IndexError, Exception) as e:
            print(f"Error during CSV to Excel conversion: {e}")
