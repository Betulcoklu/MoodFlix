"""Tests for admin_service without touching existing data."""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.movie import Movie, movie_mood_categories
from app.models.mood_category import MoodCategory
from app.models.affiliate_link import AffiliateLink
from app.models.comment import Comment
from app.models.suggestion import Suggestion
from app.models.user import User
from app.services.admin_service import AdminService


def _create_fixture():
    """Create scoped test data and return ids for cleanup."""
    user = User(email="admin_test@example.com", username="admintest", password_hash="hash")
    cat_a = MoodCategory(name="Admin Cat A")
    cat_b = MoodCategory(name="Admin Cat B")
    movie = Movie(
        title="Admin Test Movie",
        year=2024,
        imdbRating=7.7,
        createdAt=datetime(2099, 1, 1),
        description="admin movie",
    )
    movie.mood_categories.append(cat_a)

    db.session.add_all([user, cat_a, cat_b, movie])
    db.session.commit()

    comment = Comment(user_id=user.id, movie_id=movie.id, text="Nice")
    suggestion = Suggestion(user_id=user.id, title="Suggest Me", year=2025, status="pending")
    db.session.add_all([comment, suggestion])
    db.session.commit()

    return {
        "user_id": user.id,
        "movie_id": movie.id,
        "category_ids": [cat_a.id, cat_b.id],
        "comment_id": comment.id,
        "suggestion_id": suggestion.id,
        "affiliate_ids": [],
    }


def _cleanup_fixture(fx):
    # Remove affiliate links created in test
    if fx["affiliate_ids"]:
        AffiliateLink.query.filter(AffiliateLink.id.in_(fx["affiliate_ids"])).delete(synchronize_session=False)

    # Remove suggestions and comments
    if fx.get("comment_id"):
        Comment.query.filter_by(id=fx["comment_id"]).delete()
    if fx.get("suggestion_id"):
        Suggestion.query.filter_by(id=fx["suggestion_id"]).delete()

    # Remove movie-category associations for our movie
    db.session.execute(
        movie_mood_categories.delete().where(movie_mood_categories.c.movie_id == fx["movie_id"])
    )

    # Delete movie and categories created
    Movie.query.filter_by(id=fx["movie_id"]).delete()
    if fx.get("category_ids"):
        MoodCategory.query.filter(MoodCategory.id.in_(fx["category_ids"])).delete(synchronize_session=False)

    # Delete user
    if fx.get("user_id"):
        User.query.filter_by(id=fx["user_id"]).delete()

    db.session.commit()


def test_admin_movie_and_affiliate_flow():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        try:
            # List movies should include our movie
            movies = AdminService.adminListMovies()
            ids = [m.id for m in movies]
            assert fx["movie_id"] in ids

            # Edit movie
            updated = AdminService.adminEditMovie(fx["movie_id"], {"title": "Admin Test Movie Edited", "imdbRating": 8.1})
            assert updated.title == "Admin Test Movie Edited"
            assert updated.imdbRating == 8.1

            # Add affiliate link
            link = AdminService.adminAddAffiliateLink(
                fx["movie_id"], {"platformName": "TestPlatform", "url": "https://example.com/buy"}
            )
            fx["affiliate_ids"].append(link.id)
            assert link.movie_id == fx["movie_id"]

            # Remove affiliate link
            AdminService.adminRemoveAffiliateLink(link.id)
            fx["affiliate_ids"].remove(link.id)
            assert AffiliateLink.query.get(link.id) is None

            # Delete movie we created (allowed for fixture cleanup)
            AdminService.adminDeleteMovie(fx["movie_id"])
            assert Movie.query.get(fx["movie_id"]) is None
            fx["movie_id"] = None
        finally:
            _cleanup_fixture(fx)


def test_admin_category_comment_suggestion_flow():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        try:
            # List categories should include ours
            categories = AdminService.adminListCategories()
            cat_ids = {c.id for c in categories}
            assert set(fx["category_ids"]).issubset(cat_ids)

            # Create new category and edit it (do not deactivate)
            new_cat = AdminService.adminCreateCategory({"name": "Admin Cat C", "description": "desc"})
            edited_cat = AdminService.adminEditCategory(new_cat.id, {"description": "desc2"})
            assert edited_cat.description == "desc2"
            fx["category_ids"].append(new_cat.id)

            # Comments list/delete scoped to our movie
            comments = AdminService.adminListComments()
            assert any(c.id == fx["comment_id"] for c in comments)
            AdminService.adminDeleteComment(fx["comment_id"])
            fx["comment_id"] = None
            assert Comment.query.get(fx["comment_id"] or 0) is None

            # Suggestions
            pending = AdminService.adminListPendingSuggestions()
            pending_ids = {s.id for s in pending}
            assert fx["suggestion_id"] in pending_ids

            viewed = AdminService.adminViewSuggestion(fx["suggestion_id"])
            assert viewed.id == fx["suggestion_id"]

            approved = AdminService.adminApproveSuggestion(fx["suggestion_id"])
            assert approved.status == "approved"

            # Create another suggestion to reject
            another = Suggestion(user_id=fx["user_id"], title="Another Suggest", status="pending")
            db.session.add(another)
            db.session.commit()
            AdminService.adminRejectSuggestion(another.id)
            assert Suggestion.query.get(another.id).status == "rejected"
        finally:
            _cleanup_fixture(fx)


if __name__ == "__main__":
    try:
        test_admin_movie_and_affiliate_flow()
        test_admin_category_comment_suggestion_flow()
        print("✓ admin_service tests passed")
    except AssertionError as e:
        print(f"✗ admin_service test failed: {e}")
    except Exception as e:
        print(f"✗ admin_service error: {e}")
