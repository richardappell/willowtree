# test_story.py

from create_story import create_story

# Test the story generation
if __name__ == "__main__":
    try:
        result = create_story(
            child_name="Emma",
            child_age=7,
            emotion_or_theme="bravery",
            tone="magical",
            favourite_thing="unicorns",
            selected_books=["The Magic Tree House", "Harry Potter"]
        )
        
        print("Generated Story:")
        print("=" * 50)
        print(result["story"])
        print("=" * 50)
        print(f"Version: {result['version']}")
        
    except Exception as e:
        print(f"Error: {e}")