import csv
import os

CSV_FILE = "story_log.csv"

def log_story_run(version, inputs, prompt, story):
    headers = ["version", "child_name", "age", "emotion_or_theme", "tone", "favourite_thing", "selected_books", "prompt", "story"]
    
    try:
        file_exists = os.path.isfile(CSV_FILE)

        with open(CSV_FILE, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                print(f"Creating new log file: {CSV_FILE}")
                writer.writeheader()

            writer.writerow({
                "version": version,
                "child_name": inputs["child_name"],
                "age": inputs["child_age"],  # Updated to match Streamlit
                "emotion_or_theme": inputs["emotion_or_theme"],  # Updated field name
                "tone": inputs["tone"],
                "favourite_thing": inputs.get("favourite_thing", ""),  # Added favourite_thing
                "selected_books": ", ".join(inputs["selected_books"]) if inputs["selected_books"] else "",  # Updated field name
                "prompt": prompt,
                "story": story
            })

        print(f"✅ Logged story to {CSV_FILE}")

    except Exception as e:
        print(f"❌ Error logging story: {e}")