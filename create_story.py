# create_story.py

import os
import httpx
from datetime import datetime, date
from log_story_output import log_story_run

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL_NAME = "claude-3-5-sonnet-20241022"  # Faster and better than Haiku for this task

def extract_version_and_prompt():
    with open("base_prompt.txt", "r") as f:
        lines = f.readlines()
    version_line = lines[0]
    version = version_line.strip().replace("Version:", "").strip()
    prompt_text = "".join(lines[1:]).strip()
    return version, prompt_text

def calculate_age(date_of_birth):
    """Calculate age from date of birth string (YYYY-MM-DD format)"""
    if isinstance(date_of_birth, str):
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    else:
        birth_date = date_of_birth
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def create_story(child_name, date_of_birth, location, selected_books, reading_time, 
                emotional_themes, event_preparation=None, favourite_thing=None):
    version, prompt_template = extract_version_and_prompt()

    # Calculate age from date of birth
    child_age = calculate_age(date_of_birth)
    
    # Handle location
    city = location.get("city", "")
    country = location.get("country", "")
    location_str = f"{city}, {country}" if city and country else city or country or "N/A"
    
    # Handle multiple emotional themes
    if isinstance(emotional_themes, list):
        themes_str = ", ".join(emotional_themes)
    else:
        themes_str = emotional_themes or ""
    
    # Handle selected books
    books_str = ", ".join(selected_books) if selected_books else "N/A"
    
    # Handle event preparation
    event_str = event_preparation if event_preparation else "N/A"

    prompt = f"""{prompt_template}

USER INPUTS:
- Child's name: {child_name}
- Age: {child_age}
- Location: {location_str}
- Selected books (for style reference only): {books_str}
- Reading time: {reading_time}
- Emotional themes to address: {themes_str}
- Event to prepare for: {event_str}
- Favourite thing: {favourite_thing or "N/A"}
"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "max_tokens": 2048,  # Increased for longer stories
        "temperature": 0.8,   # Slightly higher for more creativity
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Increase timeout for longer story generation
        response = httpx.post(ANTHROPIC_URL, headers=headers, json=body, timeout=60.0)
        response.raise_for_status()
        
        story_text = response.json()["content"][0]["text"]
        
    except httpx.TimeoutException:
        # Retry with shorter prompt if timeout occurs
        shorter_prompt = f"""{prompt_template}

USER INPUTS:
- Child's name: {child_name}
- Age: {child_age}
- Location: {location_str}
- Reading time: {reading_time}
- Emotional themes: {themes_str}
- Event preparation: {event_str}

Create a magical story for this child focusing on joy and wonder.
"""
        
        body["messages"] = [{"role": "user", "content": shorter_prompt}]
        response = httpx.post(ANTHROPIC_URL, headers=headers, json=body, timeout=90.0)
        response.raise_for_status()
        story_text = response.json()["content"][0]["text"]
        
    except Exception as e:
        raise Exception(f"Story generation failed: {str(e)}")

    return {
        "version": version,
        "prompt": prompt,
        "story": story_text,
        "calculated_age": child_age
    }