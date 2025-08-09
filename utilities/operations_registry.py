from docx import Document
from datetime import datetime
import dateparser
import re

from operations import (
    bulk_replace,
    format_headers,
    format_body,
    update_footers,
    merge_files,
    format_specific_words,
    format_regex_matches,
    regex_replace,
    convert_to_pdf,
    date_range_validator,
    format_document,
    table_cleanup,
    extract_sections
)

# 🔧 Registry of available operations
AVAILABLE_OPERATIONS = {
    "bulk_replace": {"description": "Bulk replace text in document", "func": bulk_replace.process},
    "format_headers": {"description": "Format specified headings", "func": format_headers.process},
    "format_body": {"description": "Format body text", "func": format_body.process},
    "merge_files": {"description": "Merge all files into one", "func": merge_files.process},
    "format_specific_words": {"description": "Format specific words", "func": format_specific_words.process},
    "update_footers": {"description": "Change footer text", "func": update_footers.process},
    "format_regex_matches": {"description": "Format regex matches", "func": format_regex_matches.process},
    "regex_replace": {"description": "Regex text replace", "func": regex_replace.process},
    "convert_to_pdf": {"description": "Convert to PDF", "func": convert_to_pdf.process},
    "date_range_validator": {"description": "Validate date ranges", "func": date_range_validator.process},
    "format_document": {"description": "Document layout cleanup", "func": format_document.process},
    "table_cleanup": {"description": "Clean tables", "func": table_cleanup.process},
    "extract_sections": {"description": "Extract section(s) by heading", "func": extract_sections.process},
}


def run_operation(operation_name, doc, params):
    if operation_name not in AVAILABLE_OPERATIONS:
        return {"status": "error", "message": f"Unsupported operation: {operation_name}"}

    op_func = AVAILABLE_OPERATIONS[operation_name]["func"]

    try:
        result = op_func(doc, **params)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
