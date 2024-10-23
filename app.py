import queue
import threading
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
        self.root.title("PDF Report Extraction")

        # Set default window size (width x height)
        self.root.geometry(
            "850x275"
        )  # Set the window size to 400 pixels wide and 300 pixels tall

        # Create a button to select files
        self.select_button = tk.Button(
            root, text="Select Files", command=self.select_files
        )
        self.select_button.grid(row=0, column=0, pady=10)

        # Create a scrolled text area to display file names
        self.text_area = scrolledtext.ScrolledText(root, width=100, height=10)
        self.text_area.grid(
            row=1, column=0, pady=10, sticky="nsew"
        )  # Stretch to fill space

        # Configure grid to allow resizing
        root.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
        root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

        # Position button at the bottom right of the text area
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(
            row=2, column=0, sticky="se"
        )  # Place it below the text area

        # Create a button to copy the text area contents
        self.copy_button = tk.Button(
            self.button_frame,
            text="Copy Text",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
        )
        self.copy_button.pack(
            side=tk.RIGHT, padx=5
        )  # Align it to the right within the frame

        # Divider
        self.status_divider = tk.Frame(root, height=2, bd=1, bg="grey")
        self.status_divider.grid(row=3, column=0, sticky="ew", padx=5, pady=(10, 5))

        # Label to show status
        self.status_label = tk.Label(root, text="Ready", fg="blue")
        self.status_label.grid(
            row=4, column=0, sticky="se", padx=10, pady=5
        )  # Bottom right

        # Queue for communication between threads
        self.queue = queue.Queue()

    def select_files(self):
        # Clear the text area
        self.text_area.delete(1.0, tk.END)

        # Start a new thread for file selection to keep the GUI responsive
        threading.Thread(target=self.load_files).start()

    def load_files(self):
        # Open a file dialog to select multiple files
        file_paths = filedialog.askopenfilenames(title="Select Files")
        self.check_text()

        # Print the file names in the text area
        for index, file_path in enumerate(file_paths):
            if not (file_path.endswith(".pdf")):
                continue
            self.status_label.config(
                text=f"Processing {index + 1} of {len(file_paths)} files..."
                " Please wait."
            )
            extracted_text = extract_text_from_pdf_file(file_path)
            file_name = file_path.split("/")[-1]  # Get the file name from the full path
            output = parse_doc(file_name[:-4], extracted_text)
            self.text_area.insert(
                tk.END, output + "\n"
            )  # Insert file name into text area

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
    root = tk.Tk()
    app = FileReaderApp(root)
    root.mainloop()
