# process_plan.py

import json
from app import run_operation
from get_plan_from_gemini import get_plan_from_gemini

def process_plan(plan, src_dir, out_dir):
    """
    Execute a list of operations defined by an AI-generated plan.

    Args:
        plan (list): List of dicts {operation: str, params: dict}
        src_dir (str): Source folder path
        out_dir (str): Output folder path
    """
    results = []
    current_src_dir = src_dir  # Track which folder to read from

    for idx, step in enumerate(plan, 1):
        op = step["operation"]
        params = step.get("params", {})

        # PATCH: fix footer param name if Gemini gives wrong one:
        if op == "insert_footer" and "text" in params:
            params["footer_text"] = params.pop("text")

        print(f"\n⚙️ [{idx}/{len(plan)}] Executing '{op}' with params {params}...")
        result = run_operation(op, current_src_dir, out_dir, params)
        results.append({"operation": op, "result": result})

        # If merge_files was just run, update source dir for next steps:
        if op == "merge_files":
            current_src_dir = out_dir

    return results

if __name__ == "__main__":
    print("🔧 Document Processor AI-Orchestrated CLI 🔧\n")

    user_request = input("📝 Describe your document task:\n> ")

    print("\n🤖 Asking Gemini to interpret your request and generate a plan...")
    try:
        plan = get_plan_from_gemini(user_request)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        exit(1)

    print("\n📋 Plan received:")
    print(json.dumps(plan, indent=2))

    src_dir = "./test2"
    out_dir = "./output"

    print(f"\n📂 Processing files from '{src_dir}' → '{out_dir}'\n")
    results = process_plan(plan, src_dir, out_dir)

    print("\n✅ All operations completed. Summary:")
    for r in results:
        print(f" - {r['operation']}: {r['result']['status']}")
