# Import modules
import pandas as pd
from file_manager import FileManager


class Reader:
    def __init__(self, file_manager: FileManager, seperator: str = ';', decimal=',',
                 encoding='utf-8', engine='openpyxl'):
        """
        Initialize the Reader class with a FileManager instance.

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
        self.df = None  # Reset the DataFrame before loading new data
        try:
            # Attempt to load the CSV file
            self.df = pd.read_csv(
                file_path,
                sep=self.seperator,
                decimal=self.decimal,
                encoding=self.encoding,
                header=None
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except ValueError as e:
            raise ValueError(f"Invalid file: {file_path}") from e
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}") from e

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
            # Define the column indexes for 'Name' and 'Description'
            name_col_index = 3
            description_col_index = 17

            # Check if the column indexes are within the DataFrame's range
            if name_col_index >= self.df.shape[1] or description_col_index >= self.df.shape[1]:
                raise IndexError("Name or Description column index is out of range.")

            # Fill missing 'Name' values using the first part of the 'Description' column
            self.df.iloc[:, name_col_index] = self.df.iloc[:, name_col_index].fillna(
                self.df.iloc[:, description_col_index].apply(
                    lambda x: str(x).split(">")[0] if pd.notnull(x) else "Unknown"
                )
            )
        except Exception as e:
            print(f"An error occurred while assigning names: {e}")

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
            # Ensure names are assigned before saving to Excel
            self.assign_names()

            # Define the column indexes to be included in the output
            column_indexes = [0, 2, 3, 10, 17]

            # Select the specified columns by their index
            filtered_df = self.df.iloc[:, column_indexes]

            # Rename the columns for better readability in the Excel file
            filtered_df.columns = ['DateOfTransaction', 'IBAN', 'Name', 'Amount', 'Description']

            # Save the filtered DataFrame to an Excel file
            filtered_df.to_excel(
                f"{transactions_path}.xlsx",
                index=False,
                engine=self.engine
            )

            print(f"Successfully converted '{import_path}' to '{transactions_path}.xlsx' with selected columns.")
        except IndexError as e:
            print(f"Column index out of range: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
