# Import modules
import os
from reader import Reader


def get_file_path(year: int, month: str, base_dir: str = "data") -> str:
    """Prompt user for year and month, and construct the file path."""
    try:
        file_path = os.path.join(base_dir, str(year), f"{month}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path
    except ValueError as e:
        raise ValueError("Invalid input for year. Please enter a valid number.") from e


def write_new_file(year: int, output: str, base_dir: str = "results") -> str:
    """Prompt user to save the file and return the file path."""
    file_path = os.path.join(base_dir, str(year))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    result_path = os.path.join(file_path, output)
    return result_path


def main():
    try:
        year = int(input("Enter the year: "))
        month = input("Enter the month: ").strip()
        read_file_path = get_file_path(year, month)
        reader = Reader(read_file_path)
        # print(f"\n\n{reader.read_transactions()}")
        output = write_new_file(year, month)
        reader.save_to_excel(output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
