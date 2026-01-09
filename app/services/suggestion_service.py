"""Suggestion-related business logic."""

from datetime import datetime
from app import db
from app.models.suggestion import Suggestion
from app.models.user import User
from app.models.mood_category import MoodCategory


class SuggestionService:
    @staticmethod
    def submitSuggestion(data: dict) -> Suggestion:
        """
        Creates a new suggestion with all detailed fields.
        Expects 'data' to contain: user_id, category_id, title, year,
        description, posterUrl, imdbRating.
        """
        # 1. Validate User
        user = User.query.get(data['user_id'])
        if not user:
            raise ValueError("User not found")

        # 2. Validate Category
        # Ensure category_id is an integer
        try:
            cat_id = int(data['category_id'])
        except (ValueError, TypeError):
            raise ValueError("Invalid Category ID")

        category = MoodCategory.query.get(cat_id)
        if not category:
            raise ValueError("Mood category not found")

        # 3. Safe Type Conversion for optional fields
        year = None
        if data.get('year'):
            try:
                year = int(data['year'])
            except ValueError:
                pass
        
        rating = None
        if data.get('imdbRating'):
            try:
                rating = float(data['imdbRating'])
            except ValueError:
                pass

        # 4. Create Suggestion
        suggestion = Suggestion(
            user_id=user.id,
            mood_category_id=category.id,  # Important: Actually link the category!
            title=data['title'],
            year=year,
            description=data.get('description'),
            posterUrl=data.get('posterUrl'),
            imdbRating=rating,
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
        # Only update reviewedAt if it exists in your model (optional)
        # suggestion.reviewedAt = datetime.utcnow() 
        db.session.commit()
        return suggestion

    @staticmethod
    def rejectSuggestion(suggestionId: int) -> Suggestion:
        suggestion = Suggestion.query.get(suggestionId)
        if not suggestion:
            raise ValueError("Suggestion not found")

        suggestion.status = "rejected"
        # Only update reviewedAt if it exists in your model (optional)
        # suggestion.reviewedAt = datetime.utcnow()
        db.session.commit()
        return suggestion

    @staticmethod
    def getSuggestion(suggestionId: int) -> Suggestion | None:
        return Suggestion.query.get(suggestionId)