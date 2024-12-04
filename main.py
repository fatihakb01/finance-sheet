# Import modules
from sns import SNS
from rabo import RABO
from file_manager import FileManager


def main():
    try:
        # Prompt for year and month
        year = int(input("Enter the year: "))
        month = input("Enter the month: ").strip()
        bank = int(input(f"Choose one of the following banks:"
                         f"\n{int(1)}. SNS Bank\n{int(2)}. RABO Bank\n{int(3)}. Example Bank"
                         f"I choose option (type in a number): "))

        # Initialize FileManager and Reader
        file_manager = None
        reader = None
        if bank == 1:
            file_manager = FileManager("sns", "data", "results")
            reader = SNS(file_manager)
        elif bank == 2:
            file_manager = FileManager("rabo", "data", "results")
            reader = RABO(file_manager)
        else:
            print("Please provide a valid option (Either option 1 or 2).")

        # Get the file path and load the file
        file_path = file_manager.get_file_path(year, month)
        reader.load_file(file_path)

        # Determine output path and save the Excel file
        output = file_manager.write_new_file(year, f"{month}")
        reader.csv_to_excel(file_path, output, reader.date, reader.name, reader.amount, reader.description, reader.iban)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
