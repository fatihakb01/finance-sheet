# Import modules
import os
from reader import Reader


def get_file_path(base_dir: str = "data") -> str:
    """Prompt user for year and month, and construct the file path."""
    try:
        year = int(input("Enter the year: "))
        month = input("Enter the month: ").strip()
        file_path = os.path.join(base_dir, str(year), f"{month}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path
    except ValueError as e:
        raise ValueError("Invalid input for year. Please enter a valid number.") from e


def main():
    try:
        file_path = get_file_path()
        reader = Reader(file_path)
        print(reader.read())
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
