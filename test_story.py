# test_story.py

import json
from create_story import create_story

# Load inputs from JSON
with open("inputs/default_inputs.json") as f:
    inputs = json.load(f)

print("📝 Loaded inputs:", inputs)

try:
    # Call create_story with individual parameters (not the whole dict)
    # Map "situation" to "emotion_or_theme" to match your JSON format
    result = create_story(
        child_name=inputs.get("child_name", "Test Child"),
        child_age=inputs.get("child_age", 5),
        emotion_or_theme=inputs.get("situation", "bravery"),  # Changed from emotion_or_theme to situation
        tone=inputs.get("tone", "magical"),
        favourite_thing=inputs.get("favourite_thing", ""),
        selected_books=inputs.get("selected_books", [])
    )
    
    print("\n" + "="*50)
    print("Generated Story:")
    print("="*50)
    print(result["story"])
    print("="*50)
    print(f"Version: {result.get('version', 'Unknown')}")
    
    # Test logging if available
    try:
        from log_story_output import log_story_run
        print("\n📝 Testing logging...")
        
        # Create inputs dict that matches the logging function's expected format
        logging_inputs = {
            "child_name": inputs.get("child_name", ""),
            "child_age": inputs.get("child_age", 0),
            "emotion_or_theme": inputs.get("situation", ""),  # Map situation to emotion_or_theme
            "tone": inputs.get("tone", ""),
            "favourite_thing": inputs.get("favourite_thing", ""),
            "selected_books": inputs.get("selected_books", [])
        }
        
        log_story_run(
            version=result.get("version", "test_1.0"),
            inputs=logging_inputs,  # Use the mapped inputs
            prompt=result.get("prompt", ""),
            story=result["story"]
        )
        print("✅ Logging test completed!")
        
    except ImportError:
        print("⚠️ Logging function not available")
    except Exception as log_e:
        print(f"❌ Logging test failed: {log_e}")

except Exception as e:
    print(f"❌ Error generating story: {e}")
    import traceback
    print(f"Full error: {traceback.format_exc()}")