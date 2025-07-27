import json
import google.generativeai as genai
from keys import gemini_api_key

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def load_prompt_template():
    with open("llm_prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()

def get_plan_from_gemini(user_input):
    prompt_template = load_prompt_template()
    full_prompt = prompt_template + f"\n\nUser request:\n{user_input}"

    response = model.generate_content(full_prompt)
    text = response.text

    json_start = text.find("[")
    json_end = text.rfind("]") + 1
    plan = json.loads(text[json_start:json_end])

    return plan