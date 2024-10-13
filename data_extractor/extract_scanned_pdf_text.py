import cv2
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import numpy as np

# Set the path to the Tesseract executable if not added to PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust if necessary

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pix = page.get_pixmap()  # Convert page to pixmap
        
        # Convert the pixmap to a PIL image
        img = Image.open(io.BytesIO(pix.tobytes("png")))  
        
        # Convert PIL image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        processed_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # Resize to improve resolution
        processed_image = cv2.resize(processed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Apply Gaussian Blur to reduce noise
        processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
        
        # Apply thresholding to binarize the image
        _, binary = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Perform OCR with custom config
        custom_config = r'--oem 3 --psm 6'
        text += pytesseract.image_to_string(binary, config=custom_config)
    
    return text