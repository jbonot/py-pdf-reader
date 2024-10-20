import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

from data_extractor.doc_parser import parse_doc
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf

def extract_text_from_pdf_file(pdf_file_path):
    """Extract text from a PDF file."""
    with open(pdf_file_path, "rb") as pdf_file:
        return extract_text_from_pdf(pdf_file)
class FileReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Reader")

        # Create a button to select files
        self.select_button = tk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=10)

        # Create a scrolled text area to display file names
        self.text_area = scrolledtext.ScrolledText(root, width=40, height=10)
        self.text_area.pack(pady=10)

    def select_files(self):
        # Open a file dialog to select multiple files
        file_paths = filedialog.askopenfilenames(title="Select Files")

        # Clear the text area
        self.text_area.delete(1.0, tk.END)

        # Print the file names in the text area
        for file_path in file_paths:
            if not (file_path.endswith(".pdf")):
                continue
            extracted_text = extract_text_from_pdf_file(file_path)
            file_name = file_path.split("/")[-1]  # Get the file name from the full path
            output = parse_doc(file_name[:-4], extracted_text)
            self.text_area.insert(tk.END, output + "\n")  # Insert file name into text area

if __name__ == "__main__":
    root = tk.Tk()
    app = FileReaderApp(root)
    root.mainloop()
