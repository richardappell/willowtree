# app.py

import streamlit as st
import json
from datetime import date, datetime
from create_story import create_story

# Age-based book options from the storyboard
BOOK_OPTIONS = {
    "1-2": [
        "Brown Bear, Brown Bear, What Do You See?",
        "Goodnight Moon",
        "The Very Hungry Caterpillar",
        "Dear Zoo",
        "That's Not My...",
        "Peek-a-Boo!",
        "First 100 Words",
        "Where's Spot?",
        "Incy Wincy Spider",
        "Ten Little Fingers and Ten Little Toes"
    ],
    "2-4": [
        "Guess How Much I Love You",
        "The Very Hungry Caterpillar", 
        "Dear Zoo",
        "Owl Babies",
        "That's Not My...",
        "Each Peach Pear Plum",
        "We're Going on a Bear Hunt",
        "The Tiger Who Came to Tea",
        "Hairy Maclary from Donaldson's Dairy",
        "Rosie's Walk"
    ],
    "4-6": [
        "Room on the Broom",
        "We're Going on a Bear Hunt",
        "Where the Wild Things Are",
        "The Gruffalo",
        "Stick Man",
        "The Highway Rat",
        "Superworm",
        "Charlie and Lola",
        "Elmer the Elephant",
        "The Snowman"
    ],
    "6-8": [
        "Winnie-the-Pooh",
        "The Magic Faraway Tree",
        "Dog Man",
        "Zog",
        "Isadora Moon",
        "The BFG",
        "Fantastic Mr Fox",
        "Horrid Henry",
        "The Worst Witch",
        "Captain Underpants"
    ],
    "8-10+": [
        "Harry Potter",
        "How to Train Your Dragon",
        "The Witches",
        "Matilda",
        "Percy Jackson",
        "The Lion, the Witch and the Wardrobe",
        "Wonder",
        "Diary of a Wimpy Kid",
        "Charlotte's Web",
        "The Secret Garden"
    ]
}

EMOTIONAL_THEMES = [
    "Coping with loss",
    "Moving house or school",
    "Feeling anxious or scared",
    "Low confidence",
    "Big feelings or tantrums",
    "Starting school",
    "Making friends",
    "Learning empathy",
    "A new baby is arriving",
    "Night-time fears"
]

def get_age_from_dob(date_of_birth):
    """Calculate age from date of birth"""
    if not date_of_birth:
        return 0
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def get_age_appropriate_books(age):
    """Return book options based on age"""
    if age <= 2:
        return BOOK_OPTIONS["1-2"]
    elif age <= 4:
        return BOOK_OPTIONS["2-4"]
    elif age <= 6:
        return BOOK_OPTIONS["4-6"] 
    elif age <= 8:
        return BOOK_OPTIONS["6-8"]
    else:
        return BOOK_OPTIONS["8-10+"]

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

st.title("🌳 Willowtale Story Generator")
st.markdown("*Stories to help your child grow through what they go through.*")

st.markdown("---")

# Child Details Section
st.header("👶 Who are we writing for?")

col1, col2 = st.columns(2)
with col1:
    child_name = st.text_input("Child's name", value=defaults.get("child_name", ""))

with col2:
    # Handle date of birth from defaults
    default_dob = None
    if defaults.get("date_of_birth"):
        try:
            default_dob = datetime.strptime(defaults["date_of_birth"], "%Y-%m-%d").date()
        except:
            pass
    
    date_of_birth = st.date_input(
        "Date of birth", 
        value=default_dob,
        min_value=date(2010, 1, 1),
        max_value=date.today()
    )

col3, col4 = st.columns(2)
with col3:
    city = st.text_input("City", value=defaults.get("location", {}).get("city", ""))
with col4:
    country = st.text_input("Country", value=defaults.get("location", {}).get("country", ""))

# Calculate age and show appropriate books
if date_of_birth:
    calculated_age = get_age_from_dob(date_of_birth)
    st.info(f"Age: {calculated_age} years old")
    
    # Book Selection Section
    st.header("📚 What kinds of stories do you both love?")
    st.markdown(f"*Select up to 5 books you love reading with {child_name or 'your child'}. This helps us understand your preferred storytelling style.*")
    
    age_appropriate_books = get_age_appropriate_books(calculated_age)
    default_selected = defaults.get("selected_books", [])
    
    selected_books = st.multiselect(
        "Choose books (max 5)",
        options=age_appropriate_books,
        default=[book for book in default_selected if book in age_appropriate_books],
        max_selections=5
    )
    
    st.caption("💡 *We use these to understand tone and style - we won't copy these stories!*")
else:
    selected_books = []
    calculated_age = 0

st.markdown("---")

# Reading Time Section
st.header("⏰ When do you read stories together?")
reading_time = st.radio(
    "Reading time",
    options=["morning", "daytime", "bedtime"],
    index=["morning", "daytime", "bedtime"].index(defaults.get("reading_time", "bedtime")),
    horizontal=True
)

st.markdown("---")

# Story Purpose Section
st.header("💙 What do you hope stories can help with?")
st.markdown(f"*Sometimes stories say what we can't. What does {child_name or 'your child'} need right now?*")

# Event Preparation
event_preparation = st.text_input(
    "Is there a specific event to prepare for? (optional)",
    value=defaults.get("event_preparation", ""),
    placeholder="e.g., starting nursery, visiting grandparents, doctor's appointment"
)

# Emotional Themes
default_themes = defaults.get("emotional_themes", [])
emotional_themes = st.multiselect(
    "Select emotional themes to address (choose 1-2)",
    options=EMOTIONAL_THEMES,
    default=default_themes,
    max_selections=2
)

# Other custom theme
custom_theme = st.text_input("Something else? (optional)", placeholder="Describe in your own words...")
if custom_theme:
    emotional_themes.append(custom_theme)

# Optional Details
with st.expander("Additional details (optional)"):
    favourite_thing = st.text_input(
        "Favourite thing", 
        value=defaults.get("favourite_thing", ""),
        placeholder="e.g., dinosaurs, princesses, trains"
    )

st.markdown("---")

# Generate Story Button
if st.button("✨ Create Story", type="primary", use_container_width=True):
    if not child_name or not date_of_birth or not emotional_themes:
        st.error("Please fill in: Child's name, date of birth, and at least one emotional theme.")
    else:
        with st.spinner("Creating your personalized story... ✨"):
            try:
                location = {"city": city, "country": country}
                
                result = create_story(
                    child_name=child_name,
                    date_of_birth=date_of_birth.strftime("%Y-%m-%d"),
                    location=location,
                    selected_books=selected_books,
                    reading_time=reading_time,
                    emotional_themes=emotional_themes,
                    event_preparation=event_preparation,
                    favourite_thing=favourite_thing
                )
                
                st.success("✅ Story created successfully!")
                
                # Display the story
                st.markdown("### 📖 Your personalized story:")
                st.markdown("---")
                st.write(result["story"])
                st.markdown("---")
                
                # Log the story generation
                if LOGGING_AVAILABLE:
                    inputs = {
                        "child_name": child_name,
                        "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                        "calculated_age": result.get("calculated_age", calculated_age),
                        "location": location,
                        "selected_books": selected_books,
                        "reading_time": reading_time,
                        "emotional_themes": emotional_themes,
                        "event_preparation": event_preparation,
                        "favourite_thing": favourite_thing
                    }
                    
                    try:
                        log_story_run(
                            version=result.get("version", "1.0"),
                            inputs=inputs,
                            prompt=result.get("prompt", ""),
                            story=result["story"]
                        )
                        st.success("📝 Story logged successfully!")
                    except Exception as log_error:
                        st.error(f"❌ Logging failed: {log_error}")
                
            except Exception as e:
                st.error(f"❌ Error generating story: {e}")

# Display current defaults for reference
with st.expander("🔍 View Default Configuration"):
    st.json(defaults)