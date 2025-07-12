# operations/bulk_replace.py

from docx import Document

def process(doc, find, repl):
    """
    Replace all occurrences of `find` with `repl` in document `doc`.
    This function modifies the `doc` object in-place.
    """
    for paragraph in doc.paragraphs:
        if find in paragraph.text:
            for run in paragraph.runs:
                run.text = run.text.replace(find, repl)
