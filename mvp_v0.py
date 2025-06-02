from create_story import create_story

def main():
    print("🌱 Willowtale Story Generator")

    child_name = input("Child's name: ").strip()
    child_age = int(input("Child's age: ").strip())
    emotion_or_theme = input("What emotion or situation should the story help with?\n> ").strip()
    tone = input("Story tone (e.g., magical, comforting, funny): ").strip()
    favourite_thing = input("Child's favourite thing (e.g., unicorns, dinosaurs): ").strip()

    print("\nSelect up to 3 favourite books from the list below:")
    book_options = [
        "The Gruffalo", "Room on the Broom", "We're Going on a Bear Hunt", "Where the Wild Things Are",
        "Guess How Much I Love You", "Elmer", "Peace at Last", "The Tiger Who Came to Tea",
        "Dear Zoo", "Owl Babies", "Each Peach Pear Plum", "Monkey Puzzle",
        "The Very Hungry Caterpillar", "Brown Bear, Brown Bear", "Zog", "The Snail and the Whale",
        "Stick Man", "Not Now, Bernard", "Funnybones", "Hairy Maclary"
    ]
    for idx, book in enumerate(book_options, 1):
        print(f"{idx}. {book}")

    selected_nums = input("Enter book numbers separated by commas (e.g., 1,2,5): ").strip()
    selected_indices = [int(i)-1 for i in selected_nums.split(",") if i.strip().isdigit()]
    selected_books = [book_options[i] for i in selected_indices if 0 <= i < len(book_options)]

    story = create_story(
        child_name=child_name,
        child_age=child_age,
        emotion_or_theme=emotion_or_theme,
        tone=tone,
        favourite_thing=favourite_thing,
        selected_books=selected_books
    )

    print("\n🧚 Generated Story:")
    print("="*50)
    print(story)
    print("="*50)

if __name__ == "__main__":
    main()
