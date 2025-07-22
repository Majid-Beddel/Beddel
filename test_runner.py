import pathlib
import json
from process_plan import process_plan

# 📋 Define your manual test plan here:
plan = [
    {
        "operation": "convert_to_pdf",
        "params": {
            "use_word": True
        }
    },
    {
        "operation": "extract_sections",
        "params": {
            "target_heading": "About"
        }
    }
    # You can add more steps here
]

# 📂 Input and output folders (adjust if needed)
src_dir = pathlib.Path("./test2")       # Put test DOCX file(s) here
out_dir = pathlib.Path("./output")      # Output files go here
out_dir.mkdir(exist_ok=True)

print("🧪 Running test plan (no Gemini)...\n")
print("📋 Plan:")
print(json.dumps(plan, indent=2))

print(f"\n⚙️ Processing from '{src_dir}' to '{out_dir}'...\n")
results = process_plan(plan, src_dir, out_dir)

print("\n✅ All operations completed. Summary:")
for res in results:
    print(f" - {list(res.keys())[0]}: {list(res.values())[0]}")
