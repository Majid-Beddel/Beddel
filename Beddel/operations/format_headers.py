# operations/format_headers.py

from docx.shared import Pt, RGBColor

def process(doc, font_name=None, font_size=None, bold=None, italic=None, underline=None, color=None, heading_levels=None):
    """
    Format specified heading levels in the document.

    Args:
        doc: python-docx Document object
        font_name: Font name to apply (optional)
        font_size: Font size to apply (optional, in points)
        bold: True/False to apply bold (optional)
        italic: True/False to apply italic (optional)
        underline: True/False to apply underline (optional)
        color: tuple (R, G, B) for font color (optional)
        heading_levels: list of heading levels (e.g., [1, 2]) or None for default [1, 2, 3]
    """

    if heading_levels is None:
        heading_levels = [1, 2, 3]  # Default levels

    heading_styles = [f"Heading {level}" for level in heading_levels]

    for paragraph in doc.paragraphs:
        if paragraph.style.name in heading_styles:
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
