import pathlib
from docx import Document
import dateparser
from datetime import datetime



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
    },
    "convert_to_pdf": {
        "description": "Convert DOCX files to PDF",
        "func": convert_to_pdf.process
    },
    "date_range_validator": {  
        "description": "Check if dates are within a given range",
        "func": date_range_validator.process
    },
      "format_document": {
        "description": "Adjust layout: align text, tables, resize images",
        "func": format_document.process
    },
    "table_cleanup": {
        "description": "Clean and normalize all tables in the document",
        "func": table_cleanup.process
    },
    "extract_sections": {
        "description": "Extract a specific section by heading (e.g. About, Experience)",
        "func": extract_sections.process
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

    if operation_name == "date_range_validator":
        # ✅ Save results to DOCX report
        from docx import Document  # Local import to avoid circular dependencies
        import re
        import os

        date_pattern = r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\w+ \d{4}\b|\b\d{4}-\d{2}-\d{2}\b)"
        start = datetime.strptime(params.get("start_date"), "%Y-%m-%d")
        end = datetime.strptime(params.get("end_date"), "%Y-%m-%d")

        report_doc = Document()
        report_doc.add_heading("Date Range Validation Report", level=1)

        for file_path in docx_files:
            doc = Document(file_path)
            report_doc.add_paragraph(f"📄 File: {file_path.name}")
            out_of_range = []

            for para in doc.paragraphs:
                matches = re.findall(date_pattern, para.text)
                for match in matches:
                    parsed = dateparser.parse(match)
                    if parsed:
                        if parsed.date() < start.date() or parsed.date() > end.date():
                            out_of_range.append((match, parsed.date()))

            if out_of_range:
                for match, parsed_date in out_of_range:
                    report_doc.add_paragraph(
                        f" - ❌ '{match}' → {parsed_date} is OUTSIDE the range {start.date()} to {end.date()}"
                    )
            else:
                report_doc.add_paragraph(" - ✅ All dates within range.")

            report_doc.add_paragraph("")  # spacing

        report_path = out_path / "date_validation_report.docx"
        report_doc.save(report_path)

        return {
            "status": "success",
            "message": f"Validation complete. Report saved to {report_path.name}",
            "report_file": str(report_path)
        }

    if operation_name not in AVAILABLE_OPERATIONS:
        return {"status": "error", "message": f"Unsupported operation: {operation_name}"}

    op_func = AVAILABLE_OPERATIONS[operation_name]["func"]

    for file_path in docx_files:
        doc = Document(file_path)

        if operation_name == "convert_to_pdf":
            output_path = out_path / file_path.with_suffix(".pdf").name
            op_func(
                doc,
                input_path=file_path,
                output_path=output_path,
                use_word=params.get("use_word", False)
            )
        elif operation_name == "extract_sections":
            op_func(
                doc,
                input_path=file_path,
                out_dir=out_path,
                **params
            )
        else:
            op_func(
                doc,
                input_path=file_path,
                out_dir=out_path,
                **params
            )
            out_file = out_path / file_path.name
            doc.save(out_file)

    return {
        "status": "success",
        "files_processed": len(docx_files),
        "output_dir": str(out_path)
    }



