import json
from create_story import create_story
from log_story_output import log_story_run

# Load inputs from the JSON file
try:
    with open("inputs/default_inputs.json") as f:
        original_inputs = json.load(f)
except FileNotFoundError:
    print("Error: 'inputs/default_inputs.json' not found. Make sure the path is correct.")
    print("If 'default_inputs.json' is in the current directory, try changing the path in test_story.py.")
    exit()

# Call create_story with the new parameter structure
story_details = create_story(
    child_name=original_inputs["child_name"],
    date_of_birth=original_inputs["date_of_birth"],
    location=original_inputs["location"],
    selected_books=original_inputs.get("selected_books", []),
    reading_time=original_inputs["reading_time"],
    emotional_themes=original_inputs["emotional_themes"],
    event_preparation=original_inputs.get("event_preparation"),
    favourite_thing=original_inputs.get("favourite_thing")
)

# Print the generated story
print("\n" + "="*20 + "\nGenerated Story:\n")
print(story_details["story"])
print(f"\nCalculated age: {story_details['calculated_age']} years old")

# Log the story run
# Prepare the inputs dictionary for logging
inputs_for_logging = {
    "child_name": original_inputs["child_name"],
    "date_of_birth": original_inputs["date_of_birth"],
    "calculated_age": story_details["calculated_age"],
    "location": original_inputs["location"],
    "selected_books": original_inputs.get("selected_books", []),
    "reading_time": original_inputs["reading_time"],
    "emotional_themes": original_inputs["emotional_themes"],
    "event_preparation": original_inputs.get("event_preparation", ""),
    "favourite_thing": original_inputs.get("favourite_thing", "")
}

log_story_run(
    version=story_details["version"],
    inputs=inputs_for_logging,
    prompt=story_details["prompt"],
    story=story_details["story"]
)

print("\n✅ Story generation and logging complete.")