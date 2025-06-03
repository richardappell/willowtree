import csv
import os
import json
from datetime import datetime
import streamlit as st

# Google Sheets logging
def log_to_google_sheets(version, inputs, prompt, story):
    """Log story data to Google Sheets"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Get credentials from Streamlit secrets
        credentials_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        
        # Set up credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        
        # Open the spreadsheet (you'll need to create this and share it with your service account)
        spreadsheet_name = st.secrets.get("GOOGLE_SHEET_NAME", "Willowtale_Story_Logs")
        sheet = client.open(spreadsheet_name).sheet1
        
        # Prepare row data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle location data
        location = inputs.get("location", {})
        location_city = location.get("city", "") if isinstance(location, dict) else ""
        location_country = location.get("country", "") if isinstance(location, dict) else ""
        
        # Handle emotional themes
        emotional_themes = inputs.get("emotional_themes", [])
        if isinstance(emotional_themes, list):
            emotional_themes_str = ", ".join(emotional_themes)
        else:
            emotional_themes_str = str(emotional_themes)
        
        # Handle selected books
        selected_books = inputs.get("selected_books", [])
        selected_books_str = ", ".join(selected_books) if isinstance(selected_books, list) else str(selected_books)
        
        # Create row data
        row_data = [
            timestamp,
            version,
            inputs.get("child_name", ""),
            inputs.get("calculated_age", ""),
            inputs.get("date_of_birth", ""),
            location_city,
            location_country,
            selected_books_str,
            inputs.get("reading_time", ""),
            emotional_themes_str,
            inputs.get("event_preparation", ""),
            inputs.get("favourite_thing", ""),
            inputs.get("story_rating", ""),
            inputs.get("feedback_text", ""),
            inputs.get("feedback_timestamp", ""),
            len(prompt),
            len(story),
            prompt[:1000] + "..." if len(prompt) > 1000 else prompt,  # Truncate for sheets
            story[:2000] + "..." if len(story) > 2000 else story       # Truncate for sheets
        ]
        
        # Add row to sheet
        sheet.append_row(row_data)
        
        print("✅ Successfully logged to Google Sheets")
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets logging failed: {e}")
        return False

# CSV logging (fallback for local development)
def log_to_csv(version, inputs, prompt, story):
    """Fallback CSV logging for local development"""
    CSV_FILE = "story_log.csv"
    headers = [
        "timestamp", "version", "child_name", "calculated_age", "date_of_birth", 
        "location_city", "location_country", "selected_books", "reading_time", 
        "emotional_themes", "event_preparation", "favourite_thing", 
        "story_rating", "feedback_text", "feedback_timestamp",
        "prompt_length", "story_length", "prompt", "story"
    ]
    
    try:
        file_exists = os.path.isfile(CSV_FILE)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CSV_FILE, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            # Handle location data
            location = inputs.get("location", {})
            location_city = location.get("city", "") if isinstance(location, dict) else ""
            location_country = location.get("country", "") if isinstance(location, dict) else ""
            
            # Handle emotional themes
            emotional_themes = inputs.get("emotional_themes", [])
            if isinstance(emotional_themes, list):
                emotional_themes_str = ", ".join(emotional_themes)
            else:
                emotional_themes_str = str(emotional_themes)
            
            # Handle selected books
            selected_books = inputs.get("selected_books", [])
            selected_books_str = ", ".join(selected_books) if isinstance(selected_books, list) else str(selected_books)
            
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
                "story_rating": inputs.get("story_rating", ""),
                "feedback_text": inputs.get("feedback_text", ""),
                "feedback_timestamp": inputs.get("feedback_timestamp", ""),
                "prompt_length": len(prompt),
                "story_length": len(story),
                "prompt": prompt,
                "story": story
            }
            
            writer.writerow(row_data)
        
        print(f"✅ Logged story to {CSV_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ CSV logging failed: {e}")
        return False

def log_story_run(version, inputs, prompt, story):
    """Main logging function - tries Google Sheets first, falls back to CSV"""
    
    print(f"🔍 Starting to log story...")
    print(f"📝 Inputs received: {inputs}")
    
    # Try Google Sheets first (for production)
    try:
        if 'gcp_service_account' in st.secrets:
            success = log_to_google_sheets(version, inputs, prompt, story)
            if success:
                return
    except Exception as e:
        print(f"⚠️ Google Sheets not available: {e}")
    
    # Fallback to CSV (for local development)
    log_to_csv(version, inputs, prompt, story)

# Export function for analysis
def export_logs_to_json(output_file="story_logs_export.json"):
    """Export CSV logs to JSON format for better data analysis"""
    CSV_FILE = "story_log.csv"
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
        "favourite_thing": "unicorns",
        "story_rating": 4,
        "feedback_text": "Great story!",
        "feedback_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    log_story_run(
        version="test_v2.0",
        inputs=test_inputs,
        prompt="This is a test prompt for the new logging system",
        story="This is a test story with the updated format"
    )

if __name__ == "__main__":
    test_logging()