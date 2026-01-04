"""Favorite-related business logic."""

from typing import List

from app.extensions import db
from app.models.favorite import Favorite
from app.models.movie import Movie


def add_favorite(user_id: int, movie_id: int) -> None:
    """Add a movie to a user's favorites if not already present."""
    exists = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if exists:
        return

    fav = Favorite(user_id=user_id, movie_id=movie_id)
    db.session.add(fav)
    db.session.commit()


def remove_favorite(user_id: int, movie_id: int) -> None:
    """Remove a movie from a user's favorites if it exists."""
    fav = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not fav:
        return

    db.session.delete(fav)
    db.session.commit()


def list_user_favorites(user_id: int) -> List[Movie]:
    """List all movies favorited by a user."""
    return (
        Movie.query.join(Favorite, Favorite.movie_id == Movie.id)
        .filter(Favorite.user_id == user_id)
        .all()
    )


def is_favorite(user_id: int, movie_id: int) -> bool:
    """Check if a movie is favorited by a user."""
    return (
        Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        is not None
    )
