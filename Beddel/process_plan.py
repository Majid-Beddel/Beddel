import pathlib
import json
from operations_registry import run_operation
import google.generativeai as genai
from keys import gemini_api_key

genai.configure(api_key=gemini_api_key)  # Replace with your actual API key.
model = genai.GenerativeModel("gemini-1.5-flash")

LLM_PROMPT_FILE = "llm_prompt_template.txt"

def get_llm_prompt_template():
    try:
        with open(LLM_PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Missing prompt file: {LLM_PROMPT_FILE}")
        return ""

def plan_from_llm(user_prompt):
    template = get_llm_prompt_template()
    full_prompt = template + f"\n\nUser request: {user_prompt}"

    try:
        response = model.generate_content(full_prompt)
        text = response.text
        json_start = text.find("[")
        json_end = text.rfind("]") + 1
        plan_text = text[json_start:json_end]
        return json.loads(plan_text)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return []

def process_plan(plan, src_dir, out_dir):
    current_src_dir = src_dir
    results = []
    
    
    for idx, step in enumerate(plan):
        op = step["operation"]
        params = step.get("params", {})
        
        print(f"\n⚙️ [{idx+1}/{len(plan)}] Executing '{op}' with params {params}...")
        
        
        try:
            result = run_operation(op, current_src_dir, out_dir, params)
            results.append({op: result})
            current_src_dir = out_dir  # chain next operation on output dir
            print(f"✅ Successfully completed '{op}'")
            
        except Exception as e:
            print(f"❌ ERROR during '{op}': {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append({op: "error"})


    return results


if __name__ == "__main__":
    print("🔧 Document Processor AI-Orchestrated CLI 🔧\n")

    user_prompt = input("📝 Describe your document task:\n> ").strip()
    print("\n🤖 Asking Gemini to interpret your request and generate a plan...\n")

    plan = plan_from_llm(user_prompt)
    print("📋 Plan received:")
    print(json.dumps(plan, indent=2))

    src_dir = pathlib.Path("./test2")
    out_dir = pathlib.Path("./output")
    out_dir.mkdir(exist_ok=True)

    print(f"\n📂 Processing files from '{src_dir}' → '{out_dir}'\n")
    results = process_plan(plan, src_dir, out_dir)

    print("\n✅ All operations completed. Summary:")
    for res in results:
        print(f" - {list(res.keys())[0]}: {list(res.values())[0]}")
