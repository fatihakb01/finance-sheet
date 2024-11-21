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
            r"(\d{2}-\d{2}-\d{4})\s+(Bij|Af)\s+([\d., ]+)\s+(.*)"
        )

        # Find all transactions in the output
        transactions = transaction_pattern.findall(content)
        transaction_list = ["date, type, amount, description"]
        for match in transactions:
            transaction_list.append(f"{match[0]}, {match[1]}, {match[2]}, {match[3]}")

        return transaction_list

    def adjust_amounts(self) -> pd.DataFrame:
        """Adjust the amount column based on the type column."""
        transactions = self.read_transactions()

        if not transactions or len(transactions) <= 1:
            raise ValueError("No transactions to process.")

        # Split the header and rows
        header = transactions[0].split(", ")
        data = [row.split(", ") for row in transactions[1:]]

        # Create a DataFrame
        df = pd.DataFrame(data, columns=header)

        # Adjust the amounts
        df["amount"] = df.apply(
            lambda row: f"-{row['amount']}" if row["type"] == "Af" else row["amount"],
            axis=1,
        )

        return df

    def edit_columns(self) -> pd.DataFrame:
        """Drop the type column and create the IBAN and name columns."""
        # Recall the dataframe
        df = self.adjust_amounts()

        # Drop the type column
        df = df.drop("type", axis=1)

        # Add the IBAN column

        # Add the name column

        return df

    def save_to_excel(self, output_file: str):
        """Save the transactions to an Excel file."""
        try:
            # Adjust amounts and create a DataFrame
            df = self.edit_columns()

            # Save to Excel
            output = f"{output_file}.xlsx"
            df.to_excel(output, index=False)
            print(f"Transactions successfully saved to {output}")
        except Exception as e:
            raise Exception(f"Failed to save transactions to Excel: {e}") from e
