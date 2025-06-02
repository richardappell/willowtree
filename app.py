import streamlit as st
from create_story import create_story

st.title("Willowtale Story Generator Demo")

st.markdown("""
Fill in the details below to generate a personalised story for your child.
""")

child_name = st.text_input("Child's name")
child_age = st.number_input("Child's age", min_value=0, max_value=18, value=5)
emotion_or_theme = st.text_input("Emotion or theme (e.g. coping with change, bravery, kindness)")
tone = st.text_input("Tone (e.g. magical, funny, comforting)", value="magical")
favourite_thing = st.text_input("Favourite thing (optional)")
selected_books_raw = st.text_input("Selected books (comma-separated, optional)")

selected_books = [b.strip() for b in selected_books_raw.split(",") if b.strip()]

if st.button("Generate Story"):
    if not child_name or not emotion_or_theme or not tone:
        st.error("Please fill in the required fields: Child's name, Emotion or theme, Tone.")
    else:
        with st.spinner("Generating story..."):
            try:
                story = create_story(
                    child_name=child_name,
                    child_age=child_age,
                    emotion_or_theme=emotion_or_theme,
                    tone=tone,
                    favourite_thing=favourite_thing,
                    selected_books=selected_books
                )
                st.subheader("Your personalised story:")
                st.write(story)
            except Exception as e:
                st.error(f"Error generating story: {e}")
