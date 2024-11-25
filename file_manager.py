# Import module
import os


class FileManager:
    """
    A utility class for managing file paths and directories.
    """

    def __init__(self, base_dir="data", results_dir="results"):
        """
        Initialize the FileManager with default or custom directories.

        Parameters:
            base_dir (str): Directory containing the input files. Default is 'data'.
            results_dir (str): Directory for saving output files. Default is 'results'.
        """
        self.base_dir = base_dir
        self.results_dir = results_dir

    def get_file_path(self, year: int, month: str, file_type: str = "csv") -> str:
        """
        Construct the file path for a specific file based on year and month.

        Parameters:
            year (int): Year of the file to locate.
            month (str): Month of the file to locate.
            file_type (str): File extension/type (default is 'csv').

        Returns:
            str: The complete file path to the requested file.

        Raises:
            FileNotFoundError: If the constructed file path does not exist.
            ValueError: If invalid input is provided for the year.
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

        Creates the target directory if it does not already exist.

        Parameters:
            year (int): The year folder to organize output files.
            output (str): The name of the output file (including extension).

        Returns:
            str: The complete path where the output file will be saved.
        """
        file_path = os.path.join(self.results_dir, str(year))
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        result_path = os.path.join(file_path, output)
        return result_path
