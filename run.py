import os
from app import create_app
from app.extensions import db
from app.services.movie_service import MovieService, MOOD_GENRE_MAP
from app.models.mood_category import MoodCategory

app = create_app()

def ensure_categories_exist():
    """Checks for categories and creates them if missing."""
    if MoodCategory.query.count() == 0:
        print("🛠️  Seeding Mood Categories...")
        count = 0
        for name, genre in MOOD_GENRE_MAP.items():
            # Create category matching the Service map
            cat = MoodCategory(name=name, description=f"Movies for {name} ({genre})")
            db.session.add(cat)
            count += 1
        db.session.commit()
        print(f"✅ Created {count} categories.")
    else:
        print("✅ Categories already exist.")

if __name__ == '__main__':
    with app.app_context():
        # 1. Create Tables
        db.create_all()
        print("✅ Database tables checked/created.")

        # 2. PERMANENT FIX: Ensure Categories Exist BEFORE fetching movies
        ensure_categories_exist()

        # 3. Now it's safe to fetch movies
        MovieService.fetch_top_100()

    app.run(debug=True)