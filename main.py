import os
from data_extractor.doc_parser import parse_doc
from data_extractor.extract_pdf_text import extract_text_from_pdf
import argparse
from datetime import datetime

input_folder_path = "input"
output_folder_path = "output"

parser = argparse.ArgumentParser(description='Check for debug flag.')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

os.makedirs(output_folder_path, exist_ok=True)

if args.debug:
    debug_path = os.path.join(output_folder_path, "debug")
    os.makedirs(debug_path, exist_ok=True)

now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

for filename in os.listdir(input_folder_path):
    pdf_file_path = os.path.join(input_folder_path, filename)
    if not (os.path.isfile(pdf_file_path) and pdf_file_path.endswith(".pdf")):
        continue

    txt_file_path = os.path.join(output_folder_path, f"output_{timestamp}.txt")

    with open(pdf_file_path, "rb") as pdf_file:
        extracted_text = extract_text_from_pdf(pdf_file)
    
    if args.debug:
        debug_file_path = os.path.join(debug_path, filename[:-4] + ".txt")   
        with open(debug_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)
        print(f"--- [DEBUG] Extrated text from \"{filename}\" to \"{debug_file_path}\"")

    excel_line = parse_doc(filename[:-4], extracted_text)
    with open(txt_file_path, 'a') as file:
        file.write(excel_line + "\n")

    print(f"--- [LOG] Extrated data from \"{filename}\" to \"{txt_file_path}\"")


