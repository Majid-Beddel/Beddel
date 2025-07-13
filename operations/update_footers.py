from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx import Document

def process(doc, footer_text=None, image_path=None, image_width_in_inches=2.0):
    """
    Insert a footer into the document.
    Supports plain text and optional signature image.

    Args:
        doc: python-docx Document object
        footer_text: Optional text to include in footer
        image_path: Optional path to image (signature)
        image_width_in_inches: Width of image if provided
    """
    for section in doc.sections:
        footer = section.footer

        # 🧹 Clear existing footer paragraphs
        for paragraph in footer.paragraphs:
            p = paragraph._element
            p.getparent().remove(p)

        # ➕ Add footer text if provided
        if footer_text:
            new_para = footer.add_paragraph(footer_text)
            new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            if new_para.runs:
                run = new_para.runs[0]
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')

        # 🖼️ Add image if provided
        if image_path:
            try:
                para = footer.add_paragraph()
                run = para.add_run()
                run.add_picture(image_path, width=Inches(image_width_in_inches))
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception as e:
                print(f"⚠️ Could not add image: {e}")
