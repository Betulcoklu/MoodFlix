from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

# Ensure these imports are correct
from app.services.movie_service import MovieService
from app.services.rating_service import get_user_rating_for_movie
from app.services.comment_service import list_comments_for_movie
from app.services.favorite_service import is_favorite

movie_bp = Blueprint("movie", __name__, url_prefix="/movies")

# --- FIX 1: This route now gets ALL movies, not just homepage ones ---
@movie_bp.get("/")
def list_movies():
    # We need to make sure this method exists in your Service!
    movies = MovieService.get_all_movies() 
    # We render a dedicated list page, NOT the landing page (home.html)
    return render_template("movies/list.html", movies=movies) 

@movie_bp.get("/category/<int:category_id>")
def list_movies_by_category(category_id: int):
    sort_by = request.args.get("sort_by")
    movies = MovieService.list_movies_by_category(category_id, sort_by=sort_by)
    category = MovieService.getCategory(category_id)
    return render_template("movies/by_category.html", category=category, movies=movies, sort_by=sort_by)

@movie_bp.get("/search")
def search_movies():
    query_text = request.args.get("q", "")
    results = MovieService.search_movies_by_title(query_text) if query_text else []
    return render_template("movies/search_results.html", query=query_text, movies=results)

@movie_bp.get("/<int:movie_id>")
def view_movie_details(movie_id: int):
    try:
        movie = MovieService.get_movie_details(movie_id)
    except ValueError:
        flash("Movie not found.", "error")
        return redirect(url_for("home.index"))

    comments = list_comments_for_movie(movie_id)
    average_rating = MovieService.get_average_rating(movie_id)

    user_rating = None
    favorite_flag = False
    if current_user.is_authenticated:
        user_rating = get_user_rating_for_movie(current_user.id, movie_id)
        favorite_flag = is_favorite(current_user.id, movie_id)

    return render_template(
        "movies/detail.html",
        movie=movie,
        comments=comments,
        user_rating=user_rating,
        is_favorite=favorite_flag,
        average_rating=average_rating,
    )

@movie_bp.get("/categories")
def list_categories():
    categories = MovieService.listCategories()
    return render_template("categories/list.html", categories=categories)