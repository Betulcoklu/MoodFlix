"""Tests for rating_service."""

import sys
from pathlib import Path

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.movie import Movie
from app.models.rating import Rating
from app.services.rating_service import (
    rate_movie,
    remove_rating,
    get_user_rating_for_movie,
)


def test_rating_service_basic_flow():
    app = create_app()
    with app.app_context():
        # Clean fixtures
        Rating.query.delete()
        User.query.filter_by(email="rate@example.com").delete()
        Movie.query.filter_by(title="Rate Test Movie").delete()
        db.session.commit()

        user = User(email="rate@example.com", username="rater", password_hash="hash")
        movie = Movie(title="Rate Test Movie")
        db.session.add_all([user, movie])
        db.session.commit()

        user_id, movie_id = user.id, movie.id

        # Initially no rating
        assert get_user_rating_for_movie(user_id, movie_id) is None

        # Create rating
        rate_movie(user_id, movie_id, 4.5)
        r1 = get_user_rating_for_movie(user_id, movie_id)
        assert r1 is not None
        assert r1.value == 4.5

        # Update rating
        rate_movie(user_id, movie_id, 3.0)
        r2 = get_user_rating_for_movie(user_id, movie_id)
        assert r2 is not None
        assert r2.value == 3.0
        assert r2.updatedAt >= r1.updatedAt

        # Remove rating
        remove_rating(user_id, movie_id)
        assert get_user_rating_for_movie(user_id, movie_id) is None


if __name__ == "__main__":
    try:
        test_rating_service_basic_flow()
        print("✓ rating_service tests passed")
    except AssertionError as e:
        print(f"✗ rating_service test failed: {e}")
    except Exception as e:
        print(f"✗ rating_service error: {e}")
