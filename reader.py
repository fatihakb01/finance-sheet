# Import modules
import re
import pandas as pd
from pypdf import PdfReader


class Reader:
    def __init__(self, file_path: str):
        """Initialize the Reader with a given PDF file path."""
        self.reader = None
        try:
            self.reader = PdfReader(file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except ValueError as e:
            raise ValueError(f"Invalid file: {file_path}") from e
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}") from e

    def read_pdf(self) -> str:
        """Extract text from the first page of the PDF."""
        if not self.reader:
            raise ValueError("PDF reader is not initialized.")
        try:
            # Extract text from all pages
            all_text = []
            for i, page in enumerate(self.reader.pages):
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)
                else:
                    all_text.append(f"[Page {i + 1}: No text found]")
            return "\n\n".join(all_text)
        except IndexError as e:
            raise IndexError("PDF has no pages to read.") from e
        except Exception as e:
            raise Exception("Error while extracting text.") from e

    def read_transactions(self):
        content = self.read_pdf()

        # Regular expression to match transaction lines
        transaction_pattern = re.compile(
            r"(\d{2}-\d{2}-\d{4})\s+(Bij|Af)\s+([\d,]+)\s+(.*)"
        )

        # Find all transactions in the output
        transactions = transaction_pattern.findall(content)
        transaction_list = ["date, type, amount, description"]
        for match in transactions:
            transaction_list.append(f"{match[0]}, {match[1]}, {match[2]}, {match[3]}")

        return transaction_list

    def save_to_excel(self, output_file: str):
        """Save the transactions to an Excel file."""
        try:
            transactions = self.read_transactions()
            if not transactions or len(transactions) <= 1:
                raise ValueError("No transactions to save.")

            # Split the header and rows
            header = transactions[0].split(", ")
            data = [row.split(", ") for row in transactions[1:]]

            # Create a DataFrame
            df = pd.DataFrame(data, columns=header)

            # Save to Excel
            output = f"{output_file}.xlsx"
            df.to_excel(output, index=False)
            print(f"Transactions successfully saved to {output}")
        except Exception as e:
            raise Exception(f"Failed to save transactions to Excel: {e}") from e
