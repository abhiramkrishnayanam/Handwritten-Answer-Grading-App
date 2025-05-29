import fitz  # PyMuPDF
import os

def render_pdf_pages_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=300)
        output_path = os.path.join(output_folder, f"{pdf_name}_page_{page_number + 1}.png")
        pix.save(output_path)
        print(f"Saved page {page_number + 1} of '{pdf_name}' as image: {output_path}")
    doc.close()
