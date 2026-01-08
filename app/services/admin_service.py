"""Admin-related business logic."""

from datetime import datetime

from app import db
from app.models.movie import Movie
from app.models.mood_category import MoodCategory
from app.models.affiliate_link import AffiliateLink
from app.models.comment import Comment
from app.models.suggestion import Suggestion


class AdminService:
    @staticmethod
    def adminListMovies() -> list[Movie]:
        return Movie.query.all()

    @staticmethod
    def adminAddMovie(movieData: dict) -> Movie:
        if not movieData.get("title"):
            raise ValueError("Title is required")

        movie = Movie(
            title=movieData.get("title"),
            year=movieData.get("year"),
            description=movieData.get("description"),
            posterUrl=movieData.get("posterUrl"),
            imdbRating=movieData.get("imdbRating"),
            is_active=movieData.get("is_active", True),
        )

        category_ids = movieData.get("mood_category_ids") or []
        if category_ids:
            categories = MoodCategory.query.filter(MoodCategory.id.in_(category_ids)).all()
            for cat in categories:
                movie.mood_categories.append(cat)

        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def adminEditMovie(movieId: int, movieData: dict) -> Movie:
        movie = Movie.query.get(movieId)
        if not movie:
            raise ValueError("Movie not found")

        for field in ["title", "year", "description", "posterUrl", "imdbRating", "is_active"]:
            if field in movieData:
                setattr(movie, field, movieData[field])

        if "mood_category_ids" in movieData:
            category_ids = movieData.get("mood_category_ids") or []
            movie.mood_categories = []
            if category_ids:
                categories = MoodCategory.query.filter(MoodCategory.id.in_(category_ids)).all()
                for cat in categories:
                    movie.mood_categories.append(cat)

        db.session.commit()
        return movie

    @staticmethod
    def adminDeleteMovie(movieId: int) -> None:
        movie = Movie.query.get(movieId)
        if not movie:
            raise ValueError("Movie not found")

        db.session.delete(movie)
        db.session.commit()

    @staticmethod
    def adminAddAffiliateLink(movieId: int, linkData: dict) -> AffiliateLink:
        movie = Movie.query.get(movieId)
        if not movie:
            raise ValueError("Movie not found")

        if not linkData.get("platformName") or not linkData.get("url"):
            raise ValueError("platformName and url are required")

        link = AffiliateLink(
            movie_id=movieId,
            platformName=linkData.get("platformName"),
            url=linkData.get("url"),
            createdAt=datetime.utcnow(),
        )

        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def adminRemoveAffiliateLink(linkId: int) -> None:
        link = AffiliateLink.query.get(linkId)
        if not link:
            raise ValueError("Affiliate link not found")

        db.session.delete(link)
        db.session.commit()

    @staticmethod
    def adminListCategories() -> list[MoodCategory]:
        return MoodCategory.query.order_by(MoodCategory.name.asc()).all()

    @staticmethod
    def adminCreateCategory(categoryData: dict) -> MoodCategory:
        if not categoryData.get("name"):
            raise ValueError("Category name is required")

        category = MoodCategory(
            name=categoryData.get("name"),
            description=categoryData.get("description"),
        )
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def adminEditCategory(categoryId: int, categoryData: dict) -> MoodCategory:
        category = MoodCategory.query.get(categoryId)
        if not category:
            raise ValueError("Category not found")

        for field in ["name", "description"]:
            if field in categoryData:
                setattr(category, field, categoryData[field])

        db.session.commit()
        return category

    @staticmethod
    def adminDeactivateCategory(categoryId: int) -> None:
        category = MoodCategory.query.get(categoryId)
        if not category:
            raise ValueError("Category not found")

        for movie in list(category.movies):
            movie.mood_categories.remove(category)

        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def adminListComments(movieId: int | None = None) -> list[Comment]:
        query = Comment.query.order_by(Comment.createdAt.desc())
        if movieId is not None:
            query = query.filter_by(movie_id=movieId)
        return query.all()

    @staticmethod
    def adminDeleteComment(commentId: int) -> None:
        comment = Comment.query.get(commentId)
        if not comment:
            raise ValueError("Comment not found")

        db.session.delete(comment)
        db.session.commit()

    @staticmethod
    def adminListPendingSuggestions() -> list[Suggestion]:
        return Suggestion.query.filter_by(status="pending").order_by(Suggestion.createdAt.desc()).all()

    @staticmethod
    def adminViewSuggestion(suggestionId: int) -> Suggestion:
        suggestion = Suggestion.query.get(suggestionId)
        if not suggestion:
            raise ValueError("Suggestion not found")
        return suggestion


    @staticmethod
    def adminGetSuggestion(suggestion_id: int):
        from app.models.suggestion import Suggestion
        return Suggestion.query.get(suggestion_id)

    @staticmethod
    def adminUpdateSuggestion(suggestion_id: int, data: dict):
        from app.models.suggestion import Suggestion
        from app import db
        
        s = Suggestion.query.get(suggestion_id)
        if s:
            s.title = data['title']
            s.year = int(data['year']) if data['year'] else None
            s.mood_category_id = int(data['mood_category_id'])
            s.description = data['description']
            s.posterUrl = data['posterUrl']
            s.imdbRating = float(data['imdbRating']) if data['imdbRating'] else None
            db.session.commit()

    @staticmethod
    def adminApproveSuggestion(suggestion_id: int):
        from app.models.suggestion import Suggestion
        from app.models.movie import Movie
        from app.models.mood_category import MoodCategory
        from app import db

        # 1. Get the suggestion
        s = Suggestion.query.get(suggestion_id)
        if not s or s.status != 'pending':
            return

        # 2. Create the new Movie
        new_movie = Movie(
            title=s.title,
            year=s.year,
            description=s.description,
            posterUrl=s.posterUrl,
            imdbRating=s.imdbRating,
            is_active=True
        )

        # 3. Link the Category
        category = MoodCategory.query.get(s.mood_category_id)
        if category:
            new_movie.mood_categories.append(category)

        # 4. Update Suggestion Status
        s.status = 'approved'

        # 5. Save everything
        db.session.add(new_movie)
        db.session.commit()
    @staticmethod
    def adminRejectSuggestion(suggestionId: int) -> Suggestion:
        suggestion = Suggestion.query.get(suggestionId)
        if not suggestion:
            raise ValueError("Suggestion not found")

        suggestion.status = "rejected"
        suggestion.reviewedAt = datetime.utcnow()
        db.session.commit()
        return suggestion
