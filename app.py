# app.py

import streamlit as st
import json
from create_story import create_story

# Load default inputs
try:
    with open("inputs/default_inputs.json") as f:
        defaults = json.load(f)
    st.success("✅ Default inputs loaded")
except Exception as e:
    st.warning(f"⚠️ Could not load default inputs: {e}")
    defaults = {}

# Import the logging function
try:
    from log_story_output import log_story_run
    LOGGING_AVAILABLE = True
    st.write("✅ Logging function imported successfully")
except ImportError as e:
    st.write(f"⚠️ Could not import logging function: {e}")
    LOGGING_AVAILABLE = False

st.title("Willowtale Story Generator Demo")

st.markdown("""
Fill in the details below to generate a personalised story for your child.
""")

# Use defaults from JSON file
child_name = st.text_input("Child's name", value=defaults.get("child_name", ""))
child_age = st.number_input("Child's age", min_value=0, max_value=18, value=defaults.get("child_age", 5))
emotion_or_theme = st.text_input("Situation/Theme", value=defaults.get("situation", ""))  # Changed label to match JSON
tone = st.text_input("Tone", value=defaults.get("tone", "magical"))
favourite_thing = st.text_input("Favourite thing (optional)", value=defaults.get("favourite_thing", ""))

# Handle selected_books from JSON
default_books = ", ".join(defaults.get("selected_books", []))
selected_books_raw = st.text_input("Selected books (comma-separated, optional)", value=default_books)

selected_books = [b.strip() for b in selected_books_raw.split(",") if b.strip()]

if st.button("Generate Story"):
    if not child_name or not emotion_or_theme or not tone:
        st.error("Please fill in the required fields: Child's name, Situation/Theme, Tone.")
    else:
        with st.spinner("Generating story..."):
            try:
                result = create_story(
                    child_name=child_name,
                    child_age=child_age,
                    emotion_or_theme=emotion_or_theme,
                    tone=tone,
                    favourite_thing=favourite_thing,
                    selected_books=selected_books
                )
                
                st.subheader("Your personalised story:")
                st.write(result["story"])
                st.success("Story generated successfully!")
                
                # Log the story generation
                if LOGGING_AVAILABLE:
                    st.write("📝 Attempting to log story...")
                    inputs = {
                        "child_name": child_name,
                        "child_age": child_age,
                        "emotion_or_theme": emotion_or_theme,
                        "tone": tone,
                        "favourite_thing": favourite_thing,
                        "selected_books": selected_books
                    }
                    
                    try:
                        log_story_run(
                            version=result.get("version", "1.0"),
                            inputs=inputs,
                            prompt=result.get("prompt", ""),
                            story=result["story"]
                        )
                        st.success("✅ Story logged to CSV successfully!")
                    except Exception as log_error:
                        st.error(f"❌ Logging failed: {log_error}")
                        st.write(f"Error details: {str(log_error)}")
                else:
                    st.warning("Logging is not available")
                
            except Exception as e:
                st.error(f"Error generating story: {e}")
                st.write(f"Error details: {str(e)}")

# Display current defaults for reference
with st.expander("View Default Inputs"):
    st.json(defaults)