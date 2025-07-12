# operations/format_specific_words.py

from docx.shared import Pt, RGBColor

def process(doc, keyword=None, font_name=None, font_size=None, bold=None, italic=None, underline=None, color=None):
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
                    # No more matches, add remainder as normal run
                    remainder = text[idx:]
                    if remainder:
                        new_run = paragraph.add_run(remainder)
                        new_runs.append(new_run)
                    break
                else:
                    # Add text before match
                    if match_idx > idx:
                        before = text[idx:match_idx]
                        new_run = paragraph.add_run(before)
                        new_runs.append(new_run)

                    # Add matched keyword with formatting
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

        # After building all new runs, remove old runs
        for old_run in paragraph.runs:
            p = old_run._element
            p.getparent().remove(p)

        # Add new runs back in order
        for r in new_runs:
            paragraph._element.append(r._element)
