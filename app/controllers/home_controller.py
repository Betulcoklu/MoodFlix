from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from app.services.movie_service import MovieService
from app.services.rating_service import get_user_rating_for_movie
from app.services.comment_service import list_comments_for_movie
from app.services.favorite_service import is_favorite

home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/")
def index():
    movies = MovieService.get_movies_for_homepage()
    return render_template("home.html", movies=movies)


@home_bp.get("/categories")
def list_categories():
    categories = MovieService.listCategories()
    return render_template("categories/list.html", categories=categories)


@home_bp.get("/categories/<int:category_id>/movies")
def list_movies_by_category(category_id: int):
    sort_by = request.args.get("sort_by")
    movies = MovieService.list_movies_by_category(category_id, sort_by=sort_by)
    category = MovieService.getCategory(category_id)
    return render_template("categories/movies_by_category.html", category=category, movies=movies, sort_by=sort_by)


@home_bp.get("/search")
def search_movies():
    query_text = request.args.get("q", "")
    results = MovieService.search_movies_by_title(query_text) if query_text else []
    return render_template("search/results.html", query=query_text, movies=results)


@home_bp.get("/movies/<int:movie_id>")
def view_movie_details(movie_id: int):
    movie = MovieService.get_movie_details(movie_id)
    comments = list_comments_for_movie(movie_id)

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
    )
