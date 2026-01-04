"""Tests for movie_service (no external fetch)."""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.models.movie import Movie, movie_mood_categories
from app.models.mood_category import MoodCategory
from app.services.movie_service import MovieService


def _create_fixture():
    """Create test-only movies/categories without touching existing data."""
    c1 = MoodCategory(name="Alpha_Test")
    c2 = MoodCategory(name="Beta_Test")

    # Far future createdAt to ensure they surface first in ordering
    m1 = Movie(title="Zeta Movie Test", year=2020, imdbRating=8.5, createdAt=datetime(2100, 1, 1))
    m2 = Movie(title="alpha story test", year=2019, imdbRating=7.0, createdAt=datetime(2100, 2, 1))
    m3 = Movie(title="Beta Chronicles Test", year=2021, imdbRating=9.1, createdAt=datetime(2100, 3, 1))

    m1.mood_categories.append(c1)
    m2.mood_categories.append(c1)
    m3.mood_categories.append(c2)

    db.session.add_all([c1, c2, m1, m2, m3])
    db.session.commit()
    return {
        "category_ids": [c1.id, c2.id],
        "movie_ids": [m1.id, m2.id, m3.id],
        "objects": {"c1": c1, "c2": c2, "m1": m1, "m2": m2, "m3": m3},
    }


def _cleanup_fixture(fx):
    # Remove associations first
    db.session.execute(
        movie_mood_categories.delete().where(movie_mood_categories.c.movie_id.in_(fx["movie_ids"]))
    )
    Movie.query.filter(Movie.id.in_(fx["movie_ids"])).delete(synchronize_session=False)
    MoodCategory.query.filter(MoodCategory.id.in_(fx["category_ids"])).delete(synchronize_session=False)
    db.session.commit()


def test_list_and_get_categories():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        try:
            cats = MovieService.listCategories()
            assert any(c.name == "Alpha_Test" for c in cats)
            assert any(c.name == "Beta_Test" for c in cats)

            c1 = MovieService.getCategory(fx["objects"]["c1"].id)
            assert c1.name == "Alpha_Test"
            assert MovieService.getCategory(999999) is None
        finally:
            _cleanup_fixture(fx)


def test_list_movies_by_category_and_sorting():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        c1_id = fx["objects"]["c1"].id
        try:
            # Unsorted returns both c1 movies
            movies = MovieService.list_movies_by_category(c1_id)
            titles = {m.title for m in movies}
            assert {"Zeta Movie Test", "alpha story test"}.issubset(titles)

            # Sort by title
            by_title = MovieService.list_movies_by_category(c1_id, sort_by="title")
            our_titles = [m.title for m in by_title if m.title in {"Zeta Movie Test", "alpha story test"}]
            assert our_titles == sorted(our_titles)

            # Sort by year
            by_year = MovieService.list_movies_by_category(c1_id, sort_by="year")
            our_years = [m.year for m in by_year if m.title in {"Zeta Movie Test", "alpha story test"}]
            assert our_years == sorted(our_years)

            # Sort by rating
            by_rating = MovieService.list_movies_by_category(c1_id, sort_by="rating")
            our_ratings = [m.imdbRating for m in by_rating if m.title in {"Zeta Movie Test", "alpha story test"}]
            assert our_ratings == sorted(our_ratings)
        finally:
            _cleanup_fixture(fx)


def test_search_and_get_movie_details():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        m3 = fx["objects"]["m3"]
        try:
            results = MovieService.search_movies_by_title("beta")
            titles = [m.title for m in results]
            assert "Beta Chronicles Test" in titles
            assert MovieService.search_movies_by_title("") == []

            found = MovieService.get_movie_details(m3.id)
            assert found.title == "Beta Chronicles Test"

            try:
                MovieService.get_movie_details(999999)
                assert False, "Expected ValueError for missing movie"
            except ValueError:
                pass
        finally:
            _cleanup_fixture(fx)


def test_get_movies_for_homepage():
    app = create_app()
    with app.app_context():
        fx = _create_fixture()
        try:
            movies = MovieService.get_movies_for_homepage(limit=2)
            assert len(movies) == 2
            assert movies[0].createdAt >= movies[1].createdAt
            titles = {m.title for m in movies}
            assert titles.issubset({"Zeta Movie Test", "alpha story test", "Beta Chronicles Test"})

            assert MovieService.get_movies_for_homepage(limit=0) == []
        finally:
            _cleanup_fixture(fx)


if __name__ == "__main__":
    import traceback

    try:
        test_list_and_get_categories()
        test_list_movies_by_category_and_sorting()
        test_search_and_get_movie_details()
        test_get_movies_for_homepage()
        print("✓ movie_service tests passed (without fetching)")
    except AssertionError as e:
        print(f"✗ movie_service test failed: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"✗ movie_service error: {e}")
        traceback.print_exc()
