import pathlib
from process_plan import process_plan

plan = [
    {
        "operation": "table_cleanup",
        "params": {
            "redline": True
        }
    }
]



src_dir = pathlib.Path("./web_input")
out_dir = pathlib.Path("./web_output")
out_dir.mkdir(exist_ok=True)

print("🚀 Running test plan...")
results = process_plan(plan, src_dir, out_dir)

print("\n✅ Done. Summary:")
for r in results:
    print(f" - {list(r.keys())[0]}: {list(r.values())[0]}")
