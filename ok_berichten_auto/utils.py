import os
import re
import pytesseract
from PIL import Image, ImageGrab
from datetime import datetime

# Set up Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define application bounding box
application_bounding_box = {
    'x': 0,
    'y': 74,
    'width': 2560,
    'height': 1326
}

def activate_window(window_title_start):
    from pywinauto import Desktop
    try:
        window = Desktop(backend="uia").window(title_re=window_title_start)
        window.set_focus()
        return True
    except Exception as e:
        print(f"Window not found: {window_title_start}")
        return False

def capitalize_name(name):
    words = name.split()
    capitalized = " ".join(word.capitalize() for word in words)
    return capitalized.strip()

def load_config(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(';'):
                key, value = map(str.strip, line.split('=', 1))
                config[key] = value
    return config

def load_dates(filename):
    dates = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                fields = line.split('\t')
                date_parts = fields[1].split('/')
                dates.append({
                    'fullDate': fields[1],
                    'day': date_parts[0],
                    'month': date_parts[1],
                    'year': date_parts[2],
                    'name': fields[2]
                })
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
    screenshot = ImageGrab.grab(bbox=(bbox['x'], bbox['y'], bbox['x'] + bbox['width'], bbox['y'] + bbox['height']))
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

