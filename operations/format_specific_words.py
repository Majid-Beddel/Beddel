from docx import Document
from docx.shared import Pt, RGBColor
from pathlib import Path
import shutil

def process(input_path, output_path, keyword=None, font_name=None, font_size=None, bold=None, italic=None, underline=None, color=None, redline=False):
    doc = Document(input_path)

    if not keyword:
        return

    keyword_lower = keyword.lower()
    keyword_len = len(keyword)

    for paragraph in doc.paragraphs:
        new_runs = []

        for run in paragraph.runs:
            text = run.text
            text_lower = text.lower()

            idx = 0
            while idx < len(text):
                match_idx = text_lower.find(keyword_lower, idx)
                if match_idx == -1:
                    remainder = text[idx:]
                    if remainder:
                        new_run = paragraph.add_run(remainder)
                        new_runs.append(new_run)
                    break
                else:
                    if match_idx > idx:
                        before = text[idx:match_idx]
                        new_run = paragraph.add_run(before)
                        new_runs.append(new_run)

                    matched = text[match_idx:match_idx + keyword_len]
                    keyword_run = paragraph.add_run(matched)

                    if font_name:
                        keyword_run.font.name = font_name
                    if font_size:
                        keyword_run.font.size = Pt(font_size)
                    if bold is not None:
                        keyword_run.font.bold = bold
                    if italic is not None:
                        keyword_run.font.italic = italic
                    if underline is not None:
                        keyword_run.font.underline = underline
                    if color:
                        keyword_run.font.color.rgb = RGBColor(*color)

                    new_runs.append(keyword_run)
                    idx = match_idx + keyword_len

        for old_run in paragraph.runs:
            p = old_run._element
            p.getparent().remove(p)

        for r in new_runs:
            paragraph._element.append(r._element)

    doc.save(output_path)

    if redline:
        output_path_obj = Path(output_path)
        shutil.copy(output_path_obj, output_path_obj.parent / "redline_summary_output.docx")
