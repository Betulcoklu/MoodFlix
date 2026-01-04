"""Comment-related business logic."""

from typing import List
from datetime import datetime

from app.extensions import db
from app.models.comment import Comment


def add_comment(user_id: int, movie_id: int, text: str) -> Comment:
    """Add a new comment."""
    comment = Comment(user_id=user_id, movie_id=movie_id, text=text)
    db.session.add(comment)
    db.session.commit()
    return comment


def edit_comment(user_id: int, comment_id: int, new_text: str) -> Comment | None:
    """Edit an existing comment if owned by the user."""
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()
    if not comment:
        return None
    comment.text = new_text
    comment.updatedAt = datetime.utcnow()
    db.session.commit()
    return comment


def delete_comment(user_id: int, comment_id: int) -> None:
    """Delete a comment if owned by the user."""
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()
    if not comment:
        return
    db.session.delete(comment)
    db.session.commit()


def list_comments_for_movie(movie_id: int) -> List[Comment]:
    """List comments for a movie ordered by creation time."""
    return Comment.query.filter_by(movie_id=movie_id).order_by(Comment.createdAt.asc()).all()
