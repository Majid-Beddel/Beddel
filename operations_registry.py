import pathlib
from docx import Document

from operations import (
    bulk_replace,
    format_headers,
    format_body,
    update_footers,
    merge_files,
    format_specific_words,
    format_regex_matches,
    regex_replace
)

# 🔧 Registry of available operations
AVAILABLE_OPERATIONS = {
    "bulk_replace": {
        "description": "Bulk replace text in document",
        "func": bulk_replace.process
    },
    "format_headers": {
        "description": "Format specified headings (e.g. Heading 1, 2)",
        "func": format_headers.process
    },
    "format_body": {
        "description": "Format normal body text (non-headings)",
        "func": format_body.process
    },
    "merge_files": {
        "description": "Merge all files in folder into one document with TOC",
        "func": merge_files.process
    },
    "format_specific_words": {
        "description": "Format all occurrences of a specific word or phrase",
        "func": format_specific_words.process
    },
    "update_footers": {
        "description": "Change footer text",
        "func": update_footers.process
    },
    "format_regex_matches": {
        "description": "Format text matching a regex pattern",
        "func": format_regex_matches.process
    },
    "regex_replace": {
        "description": "Replace text matching regex pattern with repl",
        "func": regex_replace.process
    }
}

# 🔧 Shared utility used by process_plan.py:
def run_operation(operation_name, src_dir, out_dir, params):
    src_path = pathlib.Path(src_dir)
    out_path = pathlib.Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    docx_files = sorted(src_path.glob("*.docx"))
    if not docx_files:
        return {"status": "error", "message": f"No .docx files found in {src_dir}"}

    if operation_name == "merge_files":
        out_doc = Document()
        merge_files.process(docx_files, out_doc)
        out_file = out_path / "merged_files.docx"
        out_doc.save(out_file)
        return {"status": "success", "output": str(out_file)}

    if operation_name not in AVAILABLE_OPERATIONS:
        return {"status": "error", "message": f"Unsupported operation: {operation_name}"}

    op_func = AVAILABLE_OPERATIONS[operation_name]["func"]

    for file_path in docx_files:
        doc = Document(file_path)
        op_func(doc, **params)
        out_file = out_path / file_path.name
        doc.save(out_file)

    return {"status": "success", "files_processed": len(docx_files), "output_dir": str(out_path)}
