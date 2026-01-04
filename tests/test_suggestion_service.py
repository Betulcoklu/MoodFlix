"""Tests for suggestion_service."""

import sys
from pathlib import Path

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.mood_category import MoodCategory
from app.models.suggestion import Suggestion
from app.services.suggestion_service import SuggestionService


def _reset_tables():
    Suggestion.query.delete()
    User.query.delete()
    MoodCategory.query.delete()
    db.session.commit()


def test_suggestion_service_flow():
    app = create_app()
    with app.app_context():
        _reset_tables()

        user = User(email="suggest@example.com", username="suggester", password_hash="hash")
        category = MoodCategory(name="Test Category")
        db.session.add_all([user, category])
        db.session.commit()

        # Submit
        suggestion = SuggestionService.submitSuggestion(user.id, category.id, "A Movie", 2024)
        assert suggestion.status == "pending"
        assert suggestion.user_id == user.id
        assert suggestion.title == "A Movie"

        # list user and pending
        user_suggestions = SuggestionService.listUserSuggestions(user.id)
        pending = SuggestionService.listPendingSuggestions()
        assert len(user_suggestions) == 1
        assert len(pending) == 1

        # Approve
        approved = SuggestionService.approveSuggestion(suggestion.id)
        assert approved.status == "approved"
        assert approved.reviewedAt is not None
        pending_after_approve = SuggestionService.listPendingSuggestions()
        assert len(pending_after_approve) == 0

        # Reject another suggestion
        suggestion2 = SuggestionService.submitSuggestion(user.id, category.id, "Another Movie", None)
        rejected = SuggestionService.rejectSuggestion(suggestion2.id)
        assert rejected.status == "rejected"
        assert rejected.reviewedAt is not None

        # getSuggestion
        found = SuggestionService.getSuggestion(suggestion.id)
        assert found is not None
        missing = SuggestionService.getSuggestion(999999)
        assert missing is None


def test_validation_errors():
    app = create_app()
    with app.app_context():
        _reset_tables()

        user = User(email="suggest2@example.com", username="suggester2", password_hash="hash")
        category = MoodCategory(name="Test Category 2")
        db.session.add_all([user, category])
        db.session.commit()

        try:
            SuggestionService.submitSuggestion(999, category.id, "Bad User")
            assert False, "Expected ValueError for missing user"
        except ValueError:
            pass

        try:
            SuggestionService.submitSuggestion(user.id, 999, "Bad Category")
            assert False, "Expected ValueError for missing category"
        except ValueError:
            pass


if __name__ == "__main__":
    try:
        test_suggestion_service_flow()
        test_validation_errors()
        print("✓ suggestion_service tests passed")
    except AssertionError as e:
        print(f"✗ suggestion_service test failed: {e}")
    except Exception as e:
        print(f"✗ suggestion_service error: {e}")
