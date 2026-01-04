"""Rating-related business logic."""

from datetime import datetime
from typing import Optional

from app.extensions import db
from app.models.rating import Rating


def rate_movie(user_id: int, movie_id: int, value: float) -> None:
    """Create or update a user's rating for a movie."""
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if rating:
        rating.value = value
        rating.updatedAt = datetime.utcnow()
    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, value=value)
        db.session.add(rating)
    db.session.commit()


def remove_rating(user_id: int, movie_id: int) -> None:
    """Remove a user's rating for a movie if it exists."""
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rating:
        return
    db.session.delete(rating)
    db.session.commit()


def get_user_rating_for_movie(user_id: int, movie_id: int) -> Optional[Rating]:
    """Get a user's rating for a specific movie."""
    return Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
