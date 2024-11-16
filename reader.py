# Import module
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

    def read(self) -> str:
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
