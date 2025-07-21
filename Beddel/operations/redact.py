# operations/redact.py

import re

def process(doc, pattern):
    regex = re.compile(pattern)

    # Redact in paragraphs
    for para in doc.paragraphs:
        if regex.search(para.text):
            para.text = regex.sub("[REDACTED]", para.text)

    # Redact in tables too (optional but useful)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if regex.search(cell.text):
                    cell.text = regex.sub("[REDACTED]", cell.text)
