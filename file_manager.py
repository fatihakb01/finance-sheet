import os


class FileManager:
    """
    A utility class for managing file paths and directories related to banking data.

    This class provides methods to construct file paths for input and output files, ensuring proper
    organization of files based on bank name, year, and month.
    """

    def __init__(self, bank_name="sns", base_dir="data", results_dir="results"):
        """
        Initialize the FileManager with specified or default directories.

        Parameters:
            bank_name (str): Name of the bank to organize files under. Default is 'sns'.
            base_dir (str): Root directory for input files. Default is 'data'.
            results_dir (str): Root directory for saving output files. Default is 'results'.
        """
        self.bank_name = bank_name
        self.base_dir = os.path.join(base_dir, self.bank_name)
        self.results_dir = os.path.join(results_dir, self.bank_name)

    def get_file_path(self, year: int, month: str, file_type: str = "csv") -> str:
        """
        Construct the file path for an input file based on the year, month, and file type.

        Parameters:
            year (int): Year of the file to locate (e.g., 2024).
            month (str): Month of the file to locate (e.g., 'January' or '01').
            file_type (str): File extension/type (default is 'csv').

        Returns:
            str: The full file path for the requested file.

        Raises:
            FileNotFoundError: If the constructed file path does not exist.
            ValueError: If an invalid year is provided.
        """
        try:
            file_path = os.path.join(self.base_dir, str(year), f"{month}.{file_type}")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            return file_path
        except ValueError as e:
            raise ValueError("Invalid input for year. Please enter a valid number.") from e

    def write_new_file(self, year: int, output: str) -> str:
        """
        Construct the path to save a new file in the results directory.

        This method ensures the target directory exists, creating it if necessary.

        Parameters:
            year (int): The year to organize output files under (e.g., 2024).
            output (str): The name of the output file (including its extension).

        Returns:
            str: The full path where the output file will be saved.
        """
        file_path = os.path.join(self.results_dir, str(year))
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        return os.path.join(file_path, output)
