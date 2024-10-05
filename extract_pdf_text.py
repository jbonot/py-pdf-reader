import PyPDF2 # type: ignore
import os

input_folder_path = "input"
output_folder_path = "output"

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    # Iterate over all pages
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    return text

# Loop through all files in the folder
for filename in os.listdir(input_folder_path):
    pdf_file_path = os.path.join(input_folder_path, filename)
    if not (os.path.isfile(pdf_file_path) and pdf_file_path.endswith(".pdf")):
        continue

    txt_file_path = os.path.join(output_folder_path, filename[:-4] + ".txt")

    # Extract the text and write to .txt
    with open(pdf_file_path, "rb") as pdf_file:
        extracted_text = extract_text_from_pdf(pdf_file)
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(extracted_text)

    print(f"Extrated text from \"{filename}\" to \"{txt_file_path}\"")


