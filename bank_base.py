# Import module
from file_manager import FileManager
import pandas as pd


class BankBase:
    def __init__(self, file_manager: FileManager, seperator: str = ';', decimal: str = ',',
                 encoding: str = 'utf-8', engine: str = 'openpyxl', header: int = None):
        """
        Initialize the base class with shared properties.

        Parameters:
            file_manager (FileManager): Instance of FileManager to manage file paths.
            seperator (str): Delimiter used in the CSV file. Default is ';'.
            decimal (str): Decimal separator used in the CSV file. Default is ','.
            encoding (str): Character encoding of the CSV file. Default is 'utf-8'.
            engine (str): Engine used for Excel file writing. Default is 'openpyxl'.
        """
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
        Load a CSV file into a pandas DataFrame.

        Parameters:
            file_path (str): Path to the input CSV file.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
            ValueError: If the file content is invalid or unreadable.
            Exception: For any other unexpected error.
        """
        try:
            # Attempt to load the CSV file
            self.df = pd.read_csv(
                file_path,
                sep=self.seperator,
                decimal=self.decimal,
                encoding=self.encoding,
                header=self.header
            )
            if self.df.empty:
                raise ValueError(f"The file at {file_path} is empty or could not be read correctly.")

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except ValueError as e:
            raise ValueError(f"Invalid file: {file_path}") from e
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}") from e

    def assign_iban(self, iban):
        try:
            # Replace empty or NaN IBANs with 'Unknown IBAN'
            self.df.iloc[:, iban] = self.df.iloc[:, iban].apply(
                lambda x: 'Unknown IBAN' if not pd.notnull(x) or x == '' else x
            )
        except Exception as e:
            print(f"An error occurred while assigning iban: {e}")

    def create_transactions_sheet(self, date: int, name: int, amount: int, description: int, iban: int) -> pd.DataFrame:
        """
        Create a DataFrame for transactions data.
        Returns:
            pd.DataFrame: DataFrame containing the transactions.
        """
        try:
            # Assign 'Unknown IBAN' if empty
            self.assign_iban(iban)

            # Select the specified columns by their index
            column_idx = [date, iban, name, amount, description]
            filtered_df = self.df.iloc[:, column_idx]

            # Rename the columns for better readability in the Excel file
            filtered_df.columns = self.column_names

            return filtered_df
        except Exception as e:
            print(f"Error creating income-expense sheet: {e}")
            return pd.DataFrame()

    def create_income_expense_sheet(self, date: int, name: int, amount: int, description: int,
                                    iban: int) -> pd.DataFrame:
        """
        Create a DataFrame for an income-expense table based on grouped data.
        Returns:
            pd.DataFrame: DataFrame containing income and expense details.
        """
        try:
            filtered_df = self.create_transactions_sheet(date, name, amount, description, iban)

            # Group by 'Name' and 'IBAN', and sum the 'Amount'
            grouped = filtered_df.groupby(['Name', 'IBAN'])['Amount'].sum()

            # Separate into incomes and expenses
            income_df = grouped[grouped > 0].reset_index()
            income_df.columns = ['Income Names', 'IBAN', 'Income Amounts']

            expense_df = grouped[grouped < 0].reset_index()
            expense_df.columns = ['Expense Names', 'IBAN', 'Expense Amounts']

            # Ensure both income and expense tables have the same length
            max_length = max(len(income_df), len(expense_df))
            income_df = income_df.reindex(range(max_length)).fillna('')
            expense_df = expense_df.reindex(range(max_length)).fillna('')

            # Create a unified DataFrame for the income-expense table
            income_expense_df = pd.DataFrame({
                'Income Names': income_df['Income Names'],
                'Income Amounts': income_df['Income Amounts'],
                'Expense Names': expense_df['Expense Names'],
                'Expense Amounts': expense_df['Expense Amounts']
            })

            return income_expense_df
        except Exception as e:
            print(f"Error creating income-expense sheet: {e}")
            return pd.DataFrame()

    def csv_to_excel(self, import_path: str, transactions_path: str, date: int, name: int, amount: int,
                     description: int, iban: int):
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
            filtered_df = self.create_transactions_sheet(date, name, amount, description, iban)

            # Generate the income-expense table
            income_expense_df = self.create_income_expense_sheet(date, name, amount, description, iban)

            # Save both sheets to the Excel file
            with pd.ExcelWriter(f"{transactions_path}.xlsx", engine=self.engine) as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Transactions')
                income_expense_df.to_excel(writer, index=False, sheet_name='Income & Expenses')

            print(f"Successfully converted '{import_path}' to '{transactions_path}.xlsx' with selected columns.")
        except IndexError as e:
            print(f"Column index out of range: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
