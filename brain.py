import os
import time
from google import genai
from config import HOST_1_NAME, HOST_2_NAME, GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

PM_OUTLINE = [
    "1. Intro & Core Engagement Loop",
    "2. Audience & Revenue Drivers",
    "3. North Star Metric",
    "4. SWOT Analysis",
    "5. Major Product Flaws",
    "6. The Wild Feature Pitch",
    "7. Conclusion"
]

def generate_draft(company, output_dir):
    full_script = f"Topic: {company} Product Teardown\n\n"
    for i, section in enumerate(PM_OUTLINE):
        print(f"   ✍️ Writing Section {i+1}/7: {section}...")
        prompt = f"""
        Write a podcast dialogue between {HOST_1_NAME} and {HOST_2_NAME} about {company}.
        Current Section: {section}
        Script so far: {full_script}
        Format every line exactly as:
        [{HOST_1_NAME}]: <text>
        [{HOST_2_NAME}]: <text>
        """
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        
        clean_text = response.text.replace('```text', '').replace('```', '').strip()
        full_script += f"\n\n--- SECTION: {section} ---\n\n" + clean_text
        
        if i < len(PM_OUTLINE) - 1:
            print("      ⏳ Pausing 15s for API limits...")
            time.sleep(15)
            
    filepath = os.path.join(output_dir, "draft_script.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_script)

def run_ai_editor(company, editor_prompt, output_dir):
    print("\n🕵️‍♂️ AI Executive Producer is reviewing and rewriting...")
    filepath = os.path.join(output_dir, "draft_script.txt")
    
    with open(filepath, "r", encoding="utf-8") as f:
        raw_draft = f.read()
    
    formatted_prompt = editor_prompt.format(company=company) + f"\n\nRAW DRAFT:\n{raw_draft}"
    response = client.models.generate_content(model='gemini-2.5-flash', contents=formatted_prompt)
    
    clean_text = response.text.replace('```text', '').replace('```', '').strip()
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean_text)