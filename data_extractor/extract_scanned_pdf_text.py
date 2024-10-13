import cv2
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import numpy as np  # Import NumPy

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
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR on the grayscale image
        text += pytesseract.image_to_string(gray)
    
    return text