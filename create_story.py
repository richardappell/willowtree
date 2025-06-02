import os
import requests

API_KEY = os.getenv("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

def create_story(child_name, child_age, emotion_or_theme, tone, favourite_thing, selected_books, word_count=400):
    system_prompt = (
        "You are a master children’s storyteller who writes gentle, age-appropriate stories to help "
        "children process emotions and life changes. Your stories use metaphor, magic, and relatable animal or "
        "child characters. You understand child development and always write in a reassuring, emotionally safe tone for the child’s age."
    )

    user_prompt = f'''
Write a short story for a {child_age}-year-old child named {child_name}.

The story should:
- Help them process: {emotion_or_theme}
- Use a tone that is: {tone}
- Include: {favourite_thing}
- Be written in the style of: {', '.join(selected_books)}

The story should be:
- No longer than {word_count} words
- Age-appropriate in vocabulary
- Gentle and hopeful in message
- Include a clear beginning, middle, and end
- Optionally include a moral or lesson if suitable

End the story with a comforting sentence like: "And that night, they slept peacefully under the stars."
'''

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "temperature": 0.8,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} — {response.text}")

    return response.json()["content"][0]["text"]
