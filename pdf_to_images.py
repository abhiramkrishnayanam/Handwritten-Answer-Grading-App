import fitz  # PyMuPDF for PDF rendering
import os

def render_pdf_pages_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output directory if it doesn't exist

    doc = fitz.open(pdf_path)  # Open the PDF file
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Extract file name without extension

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)  # Load page by index
        pix = page.get_pixmap(dpi=300)  # Render page to image with 300 DPI
        output_path = os.path.join(output_folder, f"{pdf_name}_page_{page_number + 1}.png")  # Output file path
        pix.save(output_path)  # Save image to disk
        print(f"Saved page {page_number + 1} of '{pdf_name}' as image: {output_path}")  # Log progress

    doc.close()  # Close PDF document
