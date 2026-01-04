"""Suggestion-related business logic."""

from datetime import datetime

from app import db
from app.models.suggestion import Suggestion
from app.models.user import User
from app.models.mood_category import MoodCategory


class SuggestionService:
    @staticmethod
    def submitSuggestion(userId: int, categoryId: int, title: str, year: int | None = None) -> Suggestion:
        user = User.query.get(userId)
        if not user:
            raise ValueError("User not found")

        category = MoodCategory.query.get(categoryId)
        if not category:
            raise ValueError("Mood category not found")

        suggestion = Suggestion(
            user_id=userId,
            title=title,
            year=year,
            status="pending"
        )

        db.session.add(suggestion)
        db.session.commit()
        return suggestion

    @staticmethod
    def listUserSuggestions(userId: int) -> list[Suggestion]:
        return Suggestion.query.filter_by(user_id=userId).order_by(Suggestion.createdAt.desc()).all()

    @staticmethod
    def listPendingSuggestions() -> list[Suggestion]:
        return Suggestion.query.filter_by(status="pending").order_by(Suggestion.createdAt.desc()).all()

    @staticmethod
    def approveSuggestion(suggestionId: int) -> Suggestion:
        suggestion = Suggestion.query.get(suggestionId)
        if not suggestion:
            raise ValueError("Suggestion not found")

        suggestion.status = "approved"
        suggestion.reviewedAt = datetime.utcnow()
        db.session.commit()
        return suggestion

    @staticmethod
    def rejectSuggestion(suggestionId: int) -> Suggestion:
        suggestion = Suggestion.query.get(suggestionId)
        if not suggestion:
            raise ValueError("Suggestion not found")

        suggestion.status = "rejected"
        suggestion.reviewedAt = datetime.utcnow()
        db.session.commit()
        return suggestion

    @staticmethod
    def getSuggestion(suggestionId: int) -> Suggestion | None:
        return Suggestion.query.get(suggestionId)
