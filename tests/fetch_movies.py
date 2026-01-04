"""Script to fetch and populate movies from IMDB API."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.services.movie_service import MovieService
from app.models.movie import Movie
from app.models.mood_category import MoodCategory


def main():
    """Fetch top 100 movies and populate the database."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Fetching Top 100 Movies from IMDB API")
        print("=" * 60)
        
        # Check current state
        movie_count = Movie.query.count()
        category_count = MoodCategory.query.count()
        
        print(f"\n📊 Current database state:")
        print(f"   Movies: {movie_count}")
        print(f"   Mood Categories: {category_count}")
        
        if category_count == 0:
            print("\n⚠️  Warning: No mood categories found!")
            print("   Please run: ./.venv/bin/python tests/seed_mood_categories.py")
            return
        
        print("\n" + "-" * 60)
        
        # Fetch movies
        MovieService.fetch_top_100()
        
        print("\n" + "-" * 60)
        
        # Show final state
        final_count = Movie.query.count()
        print(f"\n✅ Final database state:")
        print(f"   Total movies: {final_count}")
        print(f"   New movies added: {final_count - movie_count}")


if __name__ == "__main__":
    main()
