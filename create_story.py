import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def create_story(inputs, prompt_template_path="prompt_templates/base_prompt.txt"):
    with open(prompt_template_path, "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        child_name=inputs["child_name"],
        child_age=inputs["child_age"],
        emotion_or_theme=inputs["emotion_or_theme"],
        tone=inputs["tone"],
        favourite_thing=inputs["favourite_thing"],
        selected_books=", ".join(inputs["selected_books"])
    )

    # Send to Claude (Haiku)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 800,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = httpx.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
    response.raise_for_status()

    return response.json()["content"][0]["text"]
