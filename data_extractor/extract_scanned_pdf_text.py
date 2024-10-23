import configparser
import io
import os

import cv2
import fitz  # PyMuPDF
import numpy as np
import pytesseract
from PIL import Image

config_file = "config.ini"
example_config_file = "config.ini.example"

config = configparser.ConfigParser()
if os.path.exists(config_file):
    config.read(config_file)
else:
    print(f"{config_file} not found. Falling back to {example_config_file}.")
    config.read(example_config_file)

try:
    pytesseract.pytesseract.tesseract_cmd = config["Tesseract"]["tesseract_cmd"]
except KeyError:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""

    # Check for available languages
    available_languages = pytesseract.get_languages(config="")
    desired_languages = ("nld", "fra")
    langs = [lang for lang in desired_languages if lang in available_languages]
    lang = "+".join(langs) or None

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pix = page.get_pixmap()  # Convert page to pixmap

        # Convert the pixmap to a PIL image
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Convert PIL image to OpenCV format
        processed_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Convert to grayscale
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

        # Resize to improve resolution
        processed_image = cv2.resize(
            processed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
        )

        # Apply thresholding to binarize the image
        _, binary = cv2.threshold(
            processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Perform OCR with custom config
        custom_config = r"--oem 3 --psm 4"
        text += pytesseract.image_to_string(binary, lang=lang, config=custom_config)

    return text
