import os
import re
import pytesseract
from PIL import Image, ImageGrab

# Set up Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define application bounding box
application_bounding_box = [0, 74, 2560, 1400]

def capitalize_name(name):
    words = name.split()
    capitalized = " ".join(word.capitalize() for word in words)
    return capitalized.strip()

def load_config(file_path):
    config = {}
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found!")

    # Read the content of the file
    with open(file_path, 'r') as file:
        config_content = file.read()

    # Initialize a dictionary to hold the config data
    config = {}

    # Split the file content into lines and process each line
    for line in config_content.splitlines():
        line = line.strip()  # Trim whitespace

        # Skip empty lines or comments (lines starting with ';')
        if not line or line.startswith(';'):
            continue

        # Split the line into key and value
        parts = line.split('=', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            config[key] = value

    return config

def load_dates(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dates file not found!")

    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content into lines
    lines = content.splitlines()

    # Initialize a list to store the date entries
    dates = []

    # Process each line
    for line in lines:
        if not line:
            continue  # Skip empty lines

        # Split the line by tab
        fields = line.split('\t')
        date = fields[0].split('/')  # Split the date part by '/'
        
        # Store the structured date data
        date_entry = {
            'fullDate': fields[0],
            'day': date[0],
            'month': date[1],
            'year': date[2],
            'name': fields[1]
        }
        dates.append(date_entry)

    return dates

def get_patient_data(text):
    match = re.match(r"(\d{1,2}j) \((\d{1,2})/(\d{1,2})/(\d{4})\) ([\w\s,]+) \((\w+)\)", text)
    if match:
        return {
            'age': match.group(1),
            'dob': f"{match.group(2)}.{match.group(3)}.{match.group(4)}",
            'name': capitalize_name(match.group(5).strip())
        }
    return None

def get_hocr_content(bbox):
    # Capture screen region specified by bounding box
    screenshot = ImageGrab.grab(bbox=(bbox['x'], bbox['y'], bbox['x'] + bbox['width'], bbox['y'] + bbox['height']))
    file_path = "tmp.png"
    screenshot.save(file_path)

    # Run Tesseract OCR to get HOCR output
    hocr_output = pytesseract.image_to_pdf_or_hocr(Image.open(file_path), extension='hocr')
    with open("output.hocr", "wb") as f:
        f.write(hocr_output)
    
    # Read and return HOCR content
    with open("output.hocr", "r", encoding='utf-8') as f:
        return f.read()

def read_text_at_position(bbox):
    # Capture screen region specified by bounding box
    screenshot = ImageGrab.grab(bbox=bbox)
    file_path = "tmp.png"
    screenshot.save(file_path)

    # Run Tesseract OCR to get plain text
    text_output = pytesseract.image_to_string(Image.open(file_path), lang="nld+fra")
    return text_output

def locate_text_at_position(target_text, bbox=application_bounding_box):
    matches = []
    hocr_content = get_hocr_content(bbox)

    # Search for target text in HOCR content using bounding box coordinates
    for match in re.finditer(r'bbox\s(\d+)\s(\d+)\s(\d+)\s(\d+).*?' + re.escape(target_text), hocr_content):
        x1, y1, x2, y2 = map(int, match.groups())
        centerX = bbox['x'] + x1 + (x2 - x1) // 2
        centerY = bbox['y'] + y1 + (y2 - y1) // 2
        matches.append({'x': centerX, 'y': centerY})
    
    return matches

