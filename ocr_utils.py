import pytesseract
import cv2
from PIL import Image
import os

# Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)
    return Image.fromarray(denoised)

def extract_text_from_images(image_folder):
    extracted_texts = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(".png"):
            path = os.path.join(image_folder, filename)
            image = preprocess_image(path)
            text = pytesseract.image_to_string(image)
            extracted_texts.append((filename, text.strip()))
    return extracted_texts
