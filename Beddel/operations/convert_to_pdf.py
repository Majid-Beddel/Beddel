import os
from docx2pdf import convert

def process(doc, input_path=None, output_path=None, use_word=False, **kwargs):
    if not input_path or not output_path:
        print("❌ Missing input or output path for PDF conversion.")
        return

    if use_word:
        print(f"📄 Using Microsoft Word (docx2pdf) to convert {input_path} → {output_path}...")

        try:
            # 🔧 Save doc in case it's been modified before PDF conversion
            doc.save(input_path)

            # Convert .docx → .pdf
            convert(input_path, output_path)
            print("✅ PDF conversion completed successfully.")

        except Exception as e:
            print(f"❌ docx2pdf failed: {e}")

    else:
        print("⚠️ LaTeX-based conversion not implemented yet (set use_word: true in your plan).")
