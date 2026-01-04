"""Script to seed mood categories into the database."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.mood_category import MoodCategory


# Define your mood categories here
categories = {
    "Make Me Cry": "Emotionally powerful stories that hit deep, pull at your heartstrings, and linger long after the credits roll.",
    "Perfect With Friends": "Easy-to-watch, entertaining picks that spark laughter, conversation, and shared moments.",
    "Mind-Bending": "Thought-provoking experiences that twist reality, challenge perception, and keep your mind engaged.",
    "Pure Fun": "Lighthearted, entertaining content made purely to relax, smile, and enjoy the moment.",
    "Hits Hard": "Intense and impactful stories that leave a strong emotional or psychological mark.",
    "Another World": "Immersive experiences that transport you into entirely different universes and atmospheres.",
    "Gets You Hyped": "High-energy, fast-paced content that fuels excitement and adrenaline.",
    "Weekend Vibes": "Feel-good, comfortable picks perfect for unwinding and enjoying a relaxed weekend mood.",
    "Adventure Overload": "Action-packed journeys filled with exploration, danger, and nonstop excitement.",
    "Date Night Picks": "Romantic or emotionally engaging choices ideal for watching together."
}



def add_mood_categories(categories_dict: dict) -> None:
    """
    Add mood categories to the database.

    Args:
        categories_dict: Dictionary with {name: description} pairs
    """
    app = create_app()
    with app.app_context():
        added_count = 0
        skipped_count = 0

        for name, description in categories_dict.items():
            # Check if category already exists
            existing = MoodCategory.query.filter_by(name=name).first()
            if existing:
                print(f"⊘ Skipped: '{name}' already exists")
                skipped_count += 1
                continue

            # Create new category
            category = MoodCategory(name=name, description=description)
            db.session.add(category)
            print(f"✓ Added: '{name}'")
            added_count += 1

        # Commit all changes
        db.session.commit()

        print(f"\n{'='*50}")
        print(f"Summary: {added_count} added, {skipped_count} skipped")
        print(f"{'='*50}")

        # Display all categories
        print("\nAll mood categories in database:")
        all_categories = MoodCategory.query.all()
        for cat in all_categories:
            print(f"  - {cat.name}: {cat.description}")


if __name__ == "__main__":
    print("="*50)
    print("Adding Mood Categories to Database")
    print("="*50)
    print()

    add_mood_categories(categories)
