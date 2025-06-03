import csv
import os
import json
from datetime import datetime

CSV_FILE = "story_log.csv"

def log_story_run(version, inputs, prompt, story):
    headers = [
        "timestamp", "version", "child_name", "calculated_age", "date_of_birth", 
        "location_city", "location_country", "selected_books", "reading_time", 
        "emotional_themes", "event_preparation", "favourite_thing", 
        "prompt_length", "story_length", "prompt", "story"
    ]
    
    print(f"🔍 Starting to log story...")
    print(f"📁 CSV file path: {os.path.abspath(CSV_FILE)}")
    print(f"📝 Inputs received: {inputs}")
    
    try:
        # Check if file exists
        file_exists = os.path.isfile(CSV_FILE)
        print(f"📂 File exists: {file_exists}")
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CSV_FILE, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                print(f"🆕 Creating new log file: {CSV_FILE}")
                writer.writeheader()
                print("✅ Header written")

            # Handle location data
            location = inputs.get("location", {})
            location_city = location.get("city", "") if isinstance(location, dict) else ""
            location_country = location.get("country", "") if isinstance(location, dict) else ""
            
            # Handle emotional themes (could be list or string)
            emotional_themes = inputs.get("emotional_themes", [])
            if isinstance(emotional_themes, list):
                emotional_themes_str = ", ".join(emotional_themes)
            else:
                emotional_themes_str = str(emotional_themes)
            
            # Handle selected books
            selected_books = inputs.get("selected_books", [])
            selected_books_str = ", ".join(selected_books) if isinstance(selected_books, list) else str(selected_books)
            
            # Prepare row data with all new fields
            row_data = {
                "timestamp": timestamp,
                "version": version,
                "child_name": inputs.get("child_name", ""),
                "calculated_age": inputs.get("calculated_age", ""),
                "date_of_birth": inputs.get("date_of_birth", ""),
                "location_city": location_city,
                "location_country": location_country,
                "selected_books": selected_books_str,
                "reading_time": inputs.get("reading_time", ""),
                "emotional_themes": emotional_themes_str,
                "event_preparation": inputs.get("event_preparation", ""),
                "favourite_thing": inputs.get("favourite_thing", ""),
                "prompt_length": len(prompt),
                "story_length": len(story),
                "prompt": prompt,  # Store full prompt for audit
                "story": story    # Store full story for audit
            }
            
            print(f"📊 Row data prepared: {list(row_data.keys())}")
            
            writer.writerow(row_data)
            print("✅ Row written to file")

        # Verify file was created/updated
        if os.path.isfile(CSV_FILE):
            file_size = os.path.getsize(CSV_FILE)
            print(f"✅ Logged story to {CSV_FILE} (File size: {file_size} bytes)")
            
            # Read and show last few lines for verification
            try:
                with open(CSV_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"📄 Total lines in file: {len(lines)}")
                    if len(lines) > 0:
                        print(f"📝 Last line written successfully")
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

def export_logs_to_json(output_file="story_logs_export.json"):
    """Export CSV logs to JSON format for better data analysis"""
    try:
        if not os.path.isfile(CSV_FILE):
            print(f"❌ No log file found at {CSV_FILE}")
            return
        
        logs = []
        with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse some fields back to appropriate types
                try:
                    row['calculated_age'] = int(row['calculated_age']) if row['calculated_age'] else None
                except ValueError:
                    row['calculated_age'] = None
                
                row['prompt_length'] = int(row['prompt_length']) if row['prompt_length'] else 0
                row['story_length'] = int(row['story_length']) if row['story_length'] else 0
                
                # Convert comma-separated strings back to lists
                if row['selected_books']:
                    row['selected_books'] = [book.strip() for book in row['selected_books'].split(',')]
                else:
                    row['selected_books'] = []
                
                if row['emotional_themes']:
                    row['emotional_themes'] = [theme.strip() for theme in row['emotional_themes'].split(',')]
                else:
                    row['emotional_themes'] = []
                
                logs.append(row)
        
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(logs, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(logs)} logs to {output_file}")
        return logs
    
    except Exception as e:
        print(f"❌ Error exporting logs: {e}")
        return None

def get_log_summary():
    """Get a summary of all logged stories"""
    try:
        if not os.path.isfile(CSV_FILE):
            return {"error": "No log file found"}
        
        with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            logs = list(reader)
        
        if not logs:
            return {"total_stories": 0}
        
        # Calculate summary statistics
        total_stories = len(logs)
        versions = list(set(log['version'] for log in logs))
        ages = [int(log['calculated_age']) for log in logs if log['calculated_age'] and log['calculated_age'].isdigit()]
        reading_times = [log['reading_time'] for log in logs if log['reading_time']]
        
        summary = {
            "total_stories": total_stories,
            "versions_used": versions,
            "age_range": {"min": min(ages), "max": max(ages)} if ages else None,
            "most_common_reading_time": max(set(reading_times), key=reading_times.count) if reading_times else None,
            "latest_story": logs[-1]['timestamp'] if logs else None,
            "earliest_story": logs[0]['timestamp'] if logs else None
        }
        
        return summary
    
    except Exception as e:
        return {"error": str(e)}

# Test function
def test_logging():
    """Test the logging function with sample data"""
    print("🧪 Testing logging function...")
    
    test_inputs = {
        "child_name": "Test Child",
        "calculated_age": 5,
        "date_of_birth": "2019-03-15",
        "location": {"city": "London", "country": "UK"},
        "selected_books": ["The Gruffalo", "Room on the Broom"],
        "reading_time": "bedtime",
        "emotional_themes": ["Starting school", "Making friends"],
        "event_preparation": "First day at reception",
        "favourite_thing": "unicorns"
    }
    
    log_story_run(
        version="test_v1.0",
        inputs=test_inputs,
        prompt="This is a test prompt for the new logging system",
        story="This is a test story with the updated format"
    )

if __name__ == "__main__":
    test_logging()
    
    # Test export functionality
    print("\n" + "="*50)
    print("Testing export functionality...")
    export_logs_to_json()
    
    # Show summary
    print("\n" + "="*50)
    print("Log Summary:")
    summary = get_log_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")