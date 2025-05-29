import pytesseract
import cv2
from PIL import Image
import os

# Set the Tesseract OCR executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Read image in color
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Apply thresholding
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)  # Denoise image
    return Image.fromarray(denoised)  # Convert to PIL Image for Tesseract

def extract_text_from_images(image_folder):
    extracted_texts = []
    for filename in sorted(os.listdir(image_folder)):  # Sort filenames for consistency
        if filename.endswith(".png"):  # Process only PNG images
            path = os.path.join(image_folder, filename)
            image = preprocess_image(path)  # Preprocess image before OCR
            text = pytesseract.image_to_string(image)  # Extract text using OCR
            extracted_texts.append((filename, text.strip()))  # Store filename and cleaned text
    return extracted_texts  # Return list of (filename, text) tuples
