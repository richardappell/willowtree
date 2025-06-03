import os
import httpx

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL_NAME = "claude-3-haiku-20240307"

def extract_version_and_prompt():
    with open("prompt_templates/base_prompt.txt", "r") as f:
        lines = f.readlines()
    version_line = lines[0]
    version = version_line.strip().replace("Version:", "").strip()
    prompt_text = "".join(lines[1:]).strip()
    return version, prompt_text

def create_story(user_inputs):
    version, prompt_template = extract_version_and_prompt()
    
    full_prompt = f"""{prompt_template}

USER INPUTS:
- Child's name: {user_inputs['child_name']}
- Age: {user_inputs['child_age']}
- Situation: {user_inputs['situation']}
- Emotional tone: {user_inputs['tone']}
- Favourite books: {', '.join(user_inputs['selected_books'])}
"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "max_tokens": 1024,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }

    response = httpx.post(ANTHROPIC_URL, headers=headers, json=body)
    response.raise_for_status()

    story_text = response.json()["content"][0]["text"]

    return version, full_prompt, story_text
