import os
import gc
import subprocess
from docx2pdf import convert
from docx import Document


def process(doc, input_path=None, output_path=None, use_word=False, **kwargs):
    if not input_path or not output_path:
        print("❌ Missing input or output path for PDF conversion.")
        return

    if use_word:
        print(f"📄 Using Microsoft Word (docx2pdf) to convert {input_path} → {output_path}...")

        try:
            doc.save(input_path)
            del doc
            doc = None
            gc.collect()

            convert(input_path, output_path)

            # 🛠 Ensure Word process doesn't keep locking the file
            subprocess.run("taskkill /f /im WINWORD.EXE", shell=True)

            print("✅ PDF conversion completed successfully.")

        except Exception as e:
            print(f"❌ docx2pdf failed: {e}")
