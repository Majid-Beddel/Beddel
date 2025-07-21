from docx import Document
from operations.extract_sections import process as extract_sections_process
import pathlib

# Setup file paths
input_path = pathlib.Path("web_input/Heading_Test.docx")
output_dir = pathlib.Path("web_output")
output_dir.mkdir(exist_ok=True)

# Load document
doc = Document(input_path)

# Print out the paragraphs for inspection
print(f"📄 Contents of {input_path}:\n")
for para in doc.paragraphs:
    print("-", para.text)

# Run extract_sections with a specific heading
extract_sections_process(
    doc,
    input_path=input_path,
    out_dir=output_dir,
    target_heading="Section One"
)

print(f"✅ Extracted section written to {output_dir}")
