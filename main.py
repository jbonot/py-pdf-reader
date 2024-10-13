import os
import argparse
from data_extractor.doc_parser import parse_doc
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf

input_folder_path = "input"
output_folder_path = "output"
output_debug_filename = "output_debug.txt"
output_filename = "output.txt"

def create_directory(path):
    """Create a directory if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)

def delete_file(directory, filename):
    path = os.path.join(directory, filename)
    try:
        os.remove(path)
        print(f"{path} has been deleted successfully.")
    except FileNotFoundError:
        pass
    except PermissionError:
        print(f"Permission denied: unable to delete {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_text_from_pdf_file(pdf_file_path):
    """Extract text from a PDF file."""
    with open(pdf_file_path, "rb") as pdf_file:
        return extract_text_from_pdf(pdf_file)

def save_debug_info(debug_path, filename, extracted_text):
    """Save extracted text to a debug file."""
    debug_file_path = os.path.join(debug_path, filename[:-4] + ".txt")
    with open(debug_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(extracted_text)
    print(f"--- [DEBUG] Extracted text from \"{filename}\" to \"{debug_file_path}\"")

def save_extracted_data(output_file_path, data):
    """Append extracted data to the output file."""
    with open(output_file_path, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def process_pdf_files(debug):
    """Process all PDF files in the input folder."""    
    for filename in os.listdir(input_folder_path):
        pdf_file_path = os.path.join(input_folder_path, filename)
        
        if not (os.path.isfile(pdf_file_path) and pdf_file_path.endswith(".pdf")):
            continue

        extracted_text = extract_text_from_pdf_file(pdf_file_path)

        if debug:
            save_debug_info(debug_path, filename, extracted_text)
            txt_file_path = os.path.join(debug_path, output_debug_filename)
        else:
            txt_file_path = os.path.join(output_folder_path, output_filename)
        
        output = parse_doc(filename[:-4], extracted_text, debug)
        save_extracted_data(txt_file_path, output)

        print(f"--- [LOG] Extracted data from \"{filename}\" to \"{txt_file_path}\"")

def reset_debug(debug_path):
    create_directory(debug_path)
    delete_file(debug_path, output_debug_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for debug flag.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    create_directory(output_folder_path)
    delete_file(output_folder_path, output_filename)

    if args.debug:
        debug_path = os.path.join(output_folder_path, "debug") if args.debug else None
        reset_debug(debug_path)

    process_pdf_files(args.debug)