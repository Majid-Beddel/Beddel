from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def process(doc, new_footer_text):
    for section in doc.sections:
        footer = section.footer

        # 🧹 Clear existing footer paragraphs
        for paragraph in footer.paragraphs:
            p = paragraph._element
            p.getparent().remove(p)

        # ➕ Add new footer paragraph
        new_para = footer.add_paragraph(new_footer_text)
        # new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 🎨 Optional: Set font styling
        if new_para.runs:
            run = new_para.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(10)
            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
