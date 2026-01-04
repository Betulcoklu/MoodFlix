"""Tests for comment_service."""

import sys
from pathlib import Path

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment
from app.services.comment_service import (
    add_comment,
    edit_comment,
    delete_comment,
    list_comments_for_movie,
)


def test_comment_service_basic_flow():
    app = create_app()
    with app.app_context():
        # Clean previous fixtures
        existing_user = User.query.filter_by(email="comment_test@example.com").first()
        if existing_user:
            Comment.query.filter_by(user_id=existing_user.id).delete()
            db.session.delete(existing_user)
            db.session.commit()

        existing_movie = Movie.query.filter_by(title="Comment Test Movie").first()
        if existing_movie:
            Comment.query.filter_by(movie_id=existing_movie.id).delete()
            db.session.delete(existing_movie)
            db.session.commit()

        user = User(email="comment_test@example.com", username="commenter", password_hash="hash")
        movie = Movie(title="Comment Test Movie")
        db.session.add_all([user, movie])
        db.session.commit()

        user_id, movie_id = user.id, movie.id

        # Add comment
        comment = add_comment(user_id, movie_id, "First!")
        assert comment is not None
        assert comment.text == "First!"

        comments = list_comments_for_movie(movie_id)
        assert len(comments) == 1
        assert comments[0].text == "First!"

        # Edit comment (owned)
        edited = edit_comment(user_id, comment.id, "Edited text")
        assert edited is not None
        assert edited.text == "Edited text"

        # Edit comment (not owned)
        other_user = User(email="other@example.com", username="other", password_hash="hash")
        db.session.add(other_user)
        db.session.commit()
        denied = edit_comment(other_user.id, comment.id, "Should not edit")
        assert denied is None

        # Delete comment (not owned)
        delete_comment(other_user.id, comment.id)
        comments_after_denied_delete = list_comments_for_movie(movie_id)
        assert len(comments_after_denied_delete) == 1

        # Delete comment (owner)
        delete_comment(user_id, comment.id)
        comments_after_delete = list_comments_for_movie(movie_id)
        assert comments_after_delete == []


def test_list_comments_ordering():
    app = create_app()
    with app.app_context():
        # Clean fixtures
        Comment.query.delete()
        db.session.commit()

        user = User(email="order@example.com", username="orderuser", password_hash="hash")
        movie = Movie(title="Ordering Movie")
        db.session.add_all([user, movie])
        db.session.commit()

        user_id, movie_id = user.id, movie.id

        add_comment(user_id, movie_id, "First")
        add_comment(user_id, movie_id, "Second")
        add_comment(user_id, movie_id, "Third")

        comments = list_comments_for_movie(movie_id)
        texts = [c.text for c in comments]
        assert texts == ["First", "Second", "Third"]


if __name__ == "__main__":
    try:
        test_comment_service_basic_flow()
        test_list_comments_ordering()
        print("✓ comment_service tests passed")
    except AssertionError as e:
        print(f"✗ comment_service test failed: {e}")
    except Exception as e:
        print(f"✗ comment_service error: {e}")
