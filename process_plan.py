# process_plan.py
from docx import Document
from io import BytesIO
from operations_registry import run_operation

def process_plan(plan, uploaded_files):
    results = []
    processed_outputs = []

    for file in uploaded_files:
        file.file.seek(0)
        doc = Document(file.file)
        original_filename = file.filename

        print(f"📄 Processing file: {original_filename}")

        try:
            for idx, step in enumerate(plan):
                op = step["operation"]
                params = step.get("params", {})
                print(f"⚙️  [{idx+1}/{len(plan)}] Executing '{op}' with params {params}...")
                run_operation(op, doc, params)

            # Save final doc to memory
            output_stream = BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)
            processed_outputs.append((original_filename, output_stream))
            results.append({original_filename: "success"})

        except Exception as e:
            print(f"❌ Error processing {original_filename}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append({original_filename: "error"})

    return processed_outputs, results
