import queue
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

from data_extractor.doc_parser import parse_doc
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf


class FileReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Report Extraction")

        # Set default window size (width x height)
        self.geometry("850x275")

        # Create a button to select files
        self.select_button = ttk.Button(
            self, text="Select Files", command=self.select_files
        )
        self.select_button.grid(row=0, column=0, pady=10)

        # Create a scrolled text area to display file names
        self.text_area = scrolledtext.ScrolledText(self, width=100, height=10)
        self.text_area.grid(row=1, column=0, pady=10, sticky="nsew")

        # Configure grid to allow resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Position button at the bottom right of the text area
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, sticky="se")

        # Create a button to copy the text area contents
        self.copy_button = ttk.Button(
            self.button_frame,
            text="Copy Text",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
        )
        self.copy_button.pack(side=tk.RIGHT, padx=5)

        # Divider
        self.status_divider = tk.Frame(self, height=2, bd=1, bg="grey")
        self.status_divider.grid(row=3, column=0, sticky="ew", padx=5, pady=(10, 5))

        # Label to show status
        self.status_label = tk.Label(self, text="Ready", fg="blue")
        self.status_label.grid(row=4, column=0, sticky="se", padx=10, pady=5)

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
        self.config(cursor="")

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
            self.clipboard_clear()
            self.clipboard_append(text.strip())
            self.copy_button.config(text="Copied!")
            self.after(2000, self.reset_button_text)

    def reset_button_text(self):
        self.copy_button.config(text="Copy Text")


if __name__ == "__main__":
    app = FileReaderApp()
    app.mainloop()
