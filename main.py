import queue
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

import TKinterModernThemes as TKMT

from data_extractor.doc_parser import parse_doc
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf


class FileReaderApp(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("PDF Report Extraction", "park", "light")

        # Configure grid to allow resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.input_frame = self.addLabelFrame("Inputs", pady=(20, 0))
        self.input_frame.Text("Select the PDFs to be processed")
        self.input_frame.nextCol()
        self.input_frame.AccentButton("Select Files", self.select_files, sticky="e")

        self.output_frame = self.addLabelFrame("Output", pady=(20, 0))
        # Create a scrolled text area to display file names
        self.text_area_frame = self.output_frame.addFrame("textarea", pady=(10, 0))
        self.text_area = scrolledtext.ScrolledText(
            self.text_area_frame.master, width=100, height=10
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        self.copy_button = self.output_frame.Button(
            "Copy Text",
            self.copy_to_clipboard,
            widgetkwargs={"state": tk.DISABLED},
            sticky="e",
        )

        self.status_frame = self.addFrame("Status", pady=(10, 10))
        self.status_label = ttk.Label(self.status_frame.master, text="Ready")
        self.status_label.grid(row=0, column=0, sticky="e")

        # Queue for communication between threads
        self.queue = queue.Queue()
        self.run()

    def select_files(self):
        # Clear the text area
        self.text_area.delete(1.0, tk.END)

        # Start a new thread for file selection to keep the GUI responsive
        threading.Thread(target=self.load_files).start()

    def load_files(self):
        # Open a file dialog to select multiple files
        file_paths = filedialog.askopenfilenames(title="Select Files")
        self.check_text()

        for index, file_path in enumerate(file_paths):
            if not (file_path.endswith(".pdf")):
                continue

            self.status_label.config(
                text=f"Processing {index + 1} of {len(file_paths)} files..."
                " Please wait."
            )

            with open(file_path, "rb") as pdf_file:
                extracted_text = extract_text_from_pdf(pdf_file)

            file_name = file_path.split("/")[-1]
            output = parse_doc(file_name[:-4], extracted_text)
            self.text_area.insert(tk.END, output + "\n")

        # Reset the status label and cursor
        self.check_text()
        self.status_label.config(text="Done.")
        self.root.config(cursor="")

    def check_text(self):
        # Check if the text area has content
        if self.text_area.get(1.0, tk.END).strip():  # Check if there's text
            self.copy_button.config(state=tk.NORMAL)  # Enable the button
        else:
            self.copy_button.config(state=tk.DISABLED)  # Disable the button

    def copy_to_clipboard(self):
        # Get the contents of the text area
        text = self.text_area.get(1.0, tk.END)  # Get all text from the text area
        # Clear the clipboard and append the new text
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text.strip())
            self.copy_button.config(text="Copied!")
            self.root.after(2000, self.reset_button_text)

    def reset_button_text(self):
        self.copy_button.config(text="Copy Text")


if __name__ == "__main__":
    app = FileReaderApp()
