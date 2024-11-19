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


def write_new_file(base_dir: str = "results") -> str:
    """Prompt user to save the file and return the file path."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    save_file = input('Do you want to save the file? (yes/no): ').strip().lower()
    if save_file == 'yes':
        file_name = input("Name of the saved file (with .csv extension): ").strip()
        file_path = os.path.join(base_dir, file_name)
        return file_path
    else:
        print("File save skipped.")


def main():
    try:
        read_file_path = get_file_path()
        reader = Reader(read_file_path)
        print(f"\n\n{reader.read_transactions()}")
        output = write_new_file()
        reader.save_to_excel(output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
