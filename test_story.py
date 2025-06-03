import json
from create_story import create_story
from log_story_output import log_story_run

# Load inputs from the JSON file
# Assuming "inputs/default_inputs.json" is the correct path relative to where you run test_story.py
# If default_inputs.json is in the same directory as test_story.py, change the path to "default_inputs.json"
try:
    with open("inputs/default_inputs.json") as f:
        original_inputs = json.load(f)
except FileNotFoundError:
    print("Error: 'inputs/default_inputs.json' not found. Make sure the path is correct.")
    print("If 'default_inputs.json' is in the current directory, try changing the path in test_story.py.")
    exit()

# 🐞 1. Correctly call create_story by unpacking the input dictionary
# Note the mapping of "situation" from JSON to the "emotion_or_theme" parameter
story_details = create_story(
    child_name=original_inputs["child_name"],
    child_age=original_inputs["child_age"],
    emotion_or_theme=original_inputs["situation"], # Map "situation" to "emotion_or_theme"
    tone=original_inputs["tone"],
    favourite_thing=original_inputs.get("favourite_thing"), # Use .get() for optional keys
    selected_books=original_inputs.get("selected_books")
)

# Print the generated story
print("\n" + "="*20 + "\nGenerated Story:\n")
print(story_details["story"])

# 🪵 2. Log the story run
# Prepare the inputs dictionary for logging, ensuring keys match those expected by log_story_run
inputs_for_logging = {
    "child_name": original_inputs["child_name"],
    "child_age": original_inputs["child_age"],
    "emotion_or_theme": original_inputs["situation"],  # Ensure this key is "emotion_or_theme" for the logger
    "tone": original_inputs["tone"],
    "favourite_thing": original_inputs.get("favourite_thing", ""), # Default to empty string if not present
    "selected_books": original_inputs.get("selected_books", []) # Default to empty list if not present
}

log_story_run(
    version=story_details["version"],
    inputs=inputs_for_logging, # Use the prepared dictionary
    prompt=story_details["prompt"],
    story=story_details["story"]
)

print("\n✅ Story generation and logging complete.")