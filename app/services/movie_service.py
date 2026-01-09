import requests
from sqlalchemy import func
from app.models.movie import Movie
from app.models.mood_category import MoodCategory
from app.models.rating import Rating
from app.models.favorite import Favorite
from app import db
from sqlalchemy import desc


MOOD_GENRE_MAP = {
    "Make Me Cry": "Drama",
    "Perfect With Friends": "Comedy",
    "Mind-Bending": "Sci-Fi",
    "Pure Fun": "Comedy",
    "Hits Hard": "Thriller",
    "Another World": "Fantasy",
    "Gets You Hyped": "Action",
    "Weekend Vibes": "Comedy",
    "Adventure Overload": "Adventure",
    "Date Night Picks": "Romance"
}


class MovieService:
    BASE_URL = "https://api.imdbapi.dev"

    
    @staticmethod
    def get_latest_movies(limit=5):
        # Sorts by Year descending, then ID descending (as a proxy for 'added recently')
        return Movie.query.filter_by(is_active=True).order_by(desc(Movie.year), desc(Movie.id)).limit(limit).all()

    @staticmethod
    def get_top_rated_movies(limit=5):
        # Sorts by IMDb rating descending
        return Movie.query.filter_by(is_active=True).order_by(desc(Movie.imdbRating)).limit(limit).all()
    
    @staticmethod
    def get_all_movies():
        # This queries ALL 42 movies without a limit
        from app.models.movie import Movie
        return Movie.query.all()
    
    @staticmethod
    def listCategories() -> list[MoodCategory]:
        return MoodCategory.query.order_by(MoodCategory.name.asc()).all()

    @staticmethod
    def getCategory(categoryId: int) -> MoodCategory | None:
        return MoodCategory.query.get(categoryId)

    @staticmethod
    def list_movies_by_category(category_id: int, sort_by: str | None = None) -> list[Movie]:
        query = Movie.query.join(Movie.mood_categories).filter(MoodCategory.id == category_id)

        sort_map = {
            "year": Movie.year,
            "title": Movie.title,
            "rating": Movie.imdbRating,
        }

        if sort_by in sort_map:
            query = query.order_by(sort_map[sort_by])

        return query.all()

    @staticmethod
    def search_movies_by_title(query_text: str) -> list[Movie]:
        if not query_text:
            return []

        pattern = f"%{query_text}%"
        return Movie.query.filter(Movie.title.ilike(pattern)).all()

    @staticmethod
    def get_movie_details(movie_id: int) -> Movie:
        movie = Movie.query.get(movie_id)
        if not movie:
            raise ValueError("Movie not found")
        return movie

    @staticmethod
    def get_average_rating(movie_id: int) -> float | None:
        avg = db.session.query(func.avg(Rating.value)).filter(Rating.movie_id == movie_id).scalar()
        return float(avg) if avg is not None else None

    @staticmethod
    def get_favorite_count(movie_id: int) -> int:
        """Return how many distinct users favorited the movie."""
        count = (
            db.session.query(func.count(func.distinct(Favorite.user_id)))
            .filter(Favorite.movie_id == movie_id)
            .scalar()
        )
        return int(count or 0)

    @staticmethod
    def get_movies_for_homepage(limit: int = 10) -> list[Movie]:
        if not limit or limit <= 0:
            return []

        return (
            Movie.query
            .order_by(Movie.createdAt.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def fetch_top_100():
        if Movie.query.count() >= 100:
            print("✅ Database already populated.")
            return

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        categories = MoodCategory.query.all()
        if not categories:
            print("❌ No mood categories found.")
            return

        total_added = 0
        movies_per_category = 10

        def extract_genres(item):
            raw = item.get("genres", [])
            genres = []
            if isinstance(raw, list):
                for entry in raw:
                    if isinstance(entry, dict):
                        text = entry.get("text") or entry.get("id")
                        if text:
                            genres.append(str(text))
                    elif entry:
                        genres.append(str(entry))
            return [g.lower() for g in genres]

        def fetch_batch(batch):
            nonlocal total_added

            batch_categories = []
            remaining = {}

            for c in batch:
                genre = MOOD_GENRE_MAP.get(c.name)
                if not genre:
                    continue

                current_count = c.movies.count()
                needed = max(0, movies_per_category - current_count)
                if needed <= 0:
                    continue

                batch_categories.append(c)
                remaining[c.id] = needed

            if not batch_categories:
                return

            genre_set = {MOOD_GENRE_MAP[c.name] for c in batch_categories}
            genre_lookup = {}
            for c in batch_categories:
                genre_lookup.setdefault(MOOD_GENRE_MAP[c.name].lower(), []).append(c)

            total_needed = sum(remaining.values())
            print(f"🔄 Fetching {total_needed} movies for batch: {[c.name for c in batch_categories]}")

            params = {
                "types": "MOVIE",
                "genre": ",".join(genre_set),
                "limit": 50,  # API limit per call
                "info": "base_info"
            }

            response = requests.get(
                f"{MovieService.BASE_URL}/titles",
                params=params,
                headers=headers
            )

            if response.status_code != 200:
                print("❌ Failed batch fetch")
                return

            movies_list = response.json().get("titles", [])

            for item in movies_list:
                if all(count == 0 for count in remaining.values()):
                    break

                item_genres = extract_genres(item)
                matched_category = None

                for g in item_genres:
                    possible_cats = genre_lookup.get(g)
                    if not possible_cats:
                        continue
                    for cat in possible_cats:
                        if remaining[cat.id] > 0:
                            matched_category = cat
                            break
                    if matched_category:
                        break

                if not matched_category:
                    continue

                title = item.get("primaryTitle")
                if not title:
                    continue

                existing_movie = Movie.query.filter_by(title=title).first()
                if existing_movie:
                    if matched_category not in existing_movie.mood_categories:
                        existing_movie.mood_categories.append(matched_category)
                        remaining[matched_category.id] -= 1
                        total_added += 1
                    continue

                new_movie = Movie(
                    title=title,
                    year=item.get("startYear"),
                    posterUrl=item.get("primaryImage", {}).get("url"),
                    imdbRating=item.get("rating", {}).get("aggregateRating", 0.0),
                    description=item.get("plot", "No description available."),
                    is_active=True
                )

                new_movie.mood_categories.append(matched_category)
                db.session.add(new_movie)

                remaining[matched_category.id] -= 1
                total_added += 1

        fetch_batch(categories[:5])
        fetch_batch(categories[5:])

        db.session.commit()
        print(f"✅ Imported {total_added} movies total.")


 