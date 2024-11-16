# Import module
from pypdf import PdfReader

# Try to get user input
try:
    year = int(input("Fill in the year: "))
    month = input("Fill in the month: ")
    reader = PdfReader(f'data/{year}/{month}.pdf')
# Raise error if there is something wrong with the user input
except ValueError as v:
    print(f"An error occurred while retrieving the year:\n{v}.")
except FileNotFoundError as f:
    print(f"An error occurred because the file does not exist:\n{f}.")
except Exception as e:
    print(f"Another error occurred:\n{e}.")
# Otherwise extract text from page
else:
    page = reader.pages[0]
    print(page.extract_text())
