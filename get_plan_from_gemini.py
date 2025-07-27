# get_plan_from_gemini.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
LLM_PROMPT_FILE = "llm_prompt_template.txt"

def get_llm_prompt_template():
    try:
        with open(LLM_PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Missing prompt file: {LLM_PROMPT_FILE}")
        return ""

async def plan_from_llm(user_prompt: str):
    template = get_llm_prompt_template()
    full_prompt = template + f"\n\nUser request: {user_prompt}"

    try:
        response = await model.generate_content_async(full_prompt)
        text = response.text
        json_start = text.find("[")
        json_end = text.rfind("]") + 1
        plan_text = text[json_start:json_end]
        return json.loads(plan_text)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return []
