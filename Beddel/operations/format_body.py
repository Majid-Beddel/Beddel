# operations/format_body.py

from docx.shared import Pt, RGBColor

def process(doc, font_name=None, font_size=None, bold=None, italic=None, underline=None, color=None):
    """
    Format normal body text (paragraphs not styled as headings) in the document.

    Args:
        doc: python-docx Document object
        font_name: Font name to apply (optional)
        font_size: Font size to apply (optional, in points)
        bold: True/False to apply bold (optional)
        italic: True/False to apply italic (optional)
        underline: True/False to apply underline (optional)
        color: tuple (R, G, B) for font color (optional)
    """

    heading_styles = [f"Heading {level}" for level in range(1, 10)]  # Cover Heading 1 to Heading 9

    for paragraph in doc.paragraphs:
        if paragraph.style.name not in heading_styles:
            for run in paragraph.runs:
                if font_name:
                    run.font.name = font_name
                if font_size:
                    run.font.size = Pt(font_size)
                if bold is not None:
                    run.font.bold = bold
                if italic is not None:
                    run.font.italic = italic
                if underline is not None:
                    run.font.underline = underline
                if color:
                    run.font.color.rgb = RGBColor(*color)
