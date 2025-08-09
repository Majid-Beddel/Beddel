from io import BytesIO
from docx import Document
from utilities.operations_registry import run_operation

def process_plan(plan, memory_files: dict) -> tuple:
    processed_outputs = []
    results = []

    for file_name, input_buffer in memory_files.items():
        try:
            print(f"📄 Processing file: {file_name}")
            doc = Document(input_buffer)

            for idx, step in enumerate(plan):
                op = step["operation"]
                params = step.get("params", {})
                print(f"⚙️  [{idx+1}/{len(plan)}] Executing '{op}' with params {params}...")
                result = run_operation(op, doc, params)
                if result.get("status") == "error":
                    raise Exception(result["message"])

            # Save processed file to memory
            output_buffer = BytesIO()
            doc.save(output_buffer)
            output_buffer.seek(0)

            processed_outputs.append((file_name, output_buffer))
            results.append({file_name: "success"})

        except Exception as e:
            print(f"❌ Error during '{op}': {e}")
            processed_outputs.append((file_name, None))
            results.append({file_name: "error"})

    return processed_outputs, results
