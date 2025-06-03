import csv
import os
from datetime import datetime

CSV_FILE = "story_log.csv"

def log_story_run(version, inputs, prompt, story):
    headers = ["timestamp", "version", "child_name", "age", "emotion_or_theme", "tone", "favourite_thing", "selected_books", "prompt", "story"]
    
    print(f"🔍 Starting to log story...")
    print(f"📁 CSV file path: {os.path.abspath(CSV_FILE)}")
    print(f"📝 Inputs received: {inputs}")
    
    try:
        # Check if file exists
        file_exists = os.path.isfile(CSV_FILE)
        print(f"📂 File exists: {file_exists}")
        
        # Get current working directory
        print(f"📍 Current working directory: {os.getcwd()}")
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CSV_FILE, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                print(f"🆕 Creating new log file: {CSV_FILE}")
                writer.writeheader()
                print("✅ Header written")

            # Prepare row data
            row_data = {
                "timestamp": timestamp,
                "version": version,
                "child_name": inputs.get("child_name", ""),
                "age": inputs.get("child_age", ""),
                "emotion_or_theme": inputs.get("emotion_or_theme", ""),
                "tone": inputs.get("tone", ""),
                "favourite_thing": inputs.get("favourite_thing", ""),
                "selected_books": ", ".join(inputs.get("selected_books", [])) if inputs.get("selected_books") else "",
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,  # Truncate long prompts
                "story": story[:10000] + "..." if len(story) > 10000 else story  # Truncate long stories
            }
            
            print(f"📊 Row data prepared: {list(row_data.keys())}")
            
            writer.writerow(row_data)
            print("✅ Row written to file")

        # Verify file was created/updated
        if os.path.isfile(CSV_FILE):
            file_size = os.path.getsize(CSV_FILE)
            print(f"✅ Logged story to {CSV_FILE} (File size: {file_size} bytes)")
            
            # Read and show last few lines
            try:
                with open(CSV_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"📄 Total lines in file: {len(lines)}")
                    if len(lines) > 0:
                        print(f"📝 Last line: {lines[-1].strip()}")
            except Exception as read_e:
                print(f"⚠️ Could not read file for verification: {read_e}")
        else:
            print("❌ File was not created!")

    except PermissionError as pe:
        print(f"❌ Permission error: {pe}")
        print("💡 Try running with administrator privileges or check file permissions")
    except Exception as e:
        print(f"❌ Error logging story: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        import traceback
        print(f"📚 Full traceback: {traceback.format_exc()}")

# Test function
def test_logging():
    """Test the logging function with sample data"""
    print("🧪 Testing logging function...")
    
    test_inputs = {
        "child_name": "Test Child",
        "child_age": 7,
        "emotion_or_theme": "test theme",
        "tone": "test tone",
        "favourite_thing": "test thing",
        "selected_books": ["Book 1", "Book 2"]
    }
    
    log_story_run(
        version="test_v1.0",
        inputs=test_inputs,
        prompt="This is a test prompt",
        story="This is a test story"
    )

if __name__ == "__main__":
    test_logging()