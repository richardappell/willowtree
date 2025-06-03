import json
from create_story import create_story

with open("inputs/default_inputs.json") as f:
    inputs = json.load(f)

story = create_story(inputs)
print("\n" + "="*20 + "\nGenerated Story:\n")
print(story)

