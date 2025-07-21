import re

def process(doc, pattern, repl):
    """
    Replace all occurrences matching regex `pattern` with `repl`.

    Args:
        doc: python-docx Document object
        pattern: regex pattern (can include flags e.g., (?i))
        repl: replacement string (can be empty to "remove")
    """
    regex = re.compile(pattern, flags=re.IGNORECASE)

    # Replace in paragraphs
    for para in doc.paragraphs:
        if regex.search(para.text):
            para.text = regex.sub(repl, para.text)

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if regex.search(cell.text):
                    cell.text = regex.sub(repl, cell.text)
