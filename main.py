# Import modules
from sns import SNS
from file_manager import FileManager


def main():
    try:
        # Prompt for year and month
        year = int(input("Enter the year: "))
        month = input("Enter the month: ").strip()

        # Initialize FileManager and Reader
        file_manager = FileManager()
        reader = SNS(file_manager)

        # Get the file path and load the file
        file_path = file_manager.get_file_path(year, month)
        reader.load_file(file_path)

        # Determine output path and save the Excel file
        output = file_manager.write_new_file(year, f"{month}")
        reader.csv_to_excel(file_path, output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
