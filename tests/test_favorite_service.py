"""Tests for favorite_service."""

import sys
from pathlib import Path

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.movie import Movie
from app.models.favorite import Favorite
from app.services.favorite_service import (
    add_favorite,
    remove_favorite,
    list_user_favorites,
    is_favorite,
)


def test_favorite_service_basic_flow():
    app = create_app()
    with app.app_context():
        # Clean any previous test data
        existing_user = User.query.filter_by(email="fav_test@example.com").first()
        if existing_user:
            Favorite.query.filter_by(user_id=existing_user.id).delete()
            db.session.delete(existing_user)
            db.session.commit()

        existing_movie = Movie.query.filter_by(title="Favorite Test Movie").first()
        if existing_movie:
            Favorite.query.filter_by(movie_id=existing_movie.id).delete()
            db.session.delete(existing_movie)
            db.session.commit()

        # Create fixtures
        user = User(email="fav_test@example.com", username="favuser", password_hash="hash")
        movie = Movie(title="Favorite Test Movie")
        db.session.add_all([user, movie])
        db.session.commit()

        user_id, movie_id = user.id, movie.id

        # Initial state
        assert is_favorite(user_id, movie_id) is False
        assert list_user_favorites(user_id) == []

        # Add favorite
        add_favorite(user_id, movie_id)
        assert is_favorite(user_id, movie_id) is True
        favorites = list_user_favorites(user_id)
        assert len(favorites) == 1
        assert favorites[0].id == movie_id

        # Idempotent add
        add_favorite(user_id, movie_id)
        favorites_again = list_user_favorites(user_id)
        assert len(favorites_again) == 1

        # Remove
        remove_favorite(user_id, movie_id)
        assert is_favorite(user_id, movie_id) is False
        assert list_user_favorites(user_id) == []


if __name__ == "__main__":
    # Allow running directly for quick checks
    try:
        test_favorite_service_basic_flow()
        print("✓ favorite_service tests passed")
    except AssertionError as e:
        print(f"✗ favorite_service test failed: {e}")
    except Exception as e:
        print(f"✗ favorite_service error: {e}")
