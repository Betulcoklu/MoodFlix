from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user

from app.services.favorite_service import add_favorite, remove_favorite, list_user_favorites

favorite_bp = Blueprint("favorite", __name__, url_prefix="/favorites")


@favorite_bp.get("/")
def list_favorites():
    if not current_user.is_authenticated:
        flash("Please log in to view favorites.", "error")
        return redirect(url_for("auth.login"))

    favorites = list_user_favorites(current_user.id)
    
    # FIX 1: Render the template instead of returning a dictionary
    return render_template("favorites/list.html", movies=favorites)


@favorite_bp.post("/add/<int:movie_id>")
def add_favorite_route(movie_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to favorite movies.", "error")
        return redirect(url_for("auth.login"))

    add_favorite(current_user.id, movie_id)
    flash("Added to favorites.", "success")
    
    # FIX 2: Redirect back to the movie details (better UX)
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))


@favorite_bp.post("/remove/<int:movie_id>")
def remove_favorite_route(movie_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to update favorites.", "error")
        return redirect(url_for("auth.login"))

    remove_favorite(current_user.id, movie_id)
    flash("Removed from favorites.", "info")
    
    # Logic: If we are on the Favorites page, stay there. 
    # If we are on the Movie Detail page, stay there.
    # We use 'request.referrer' to check where the user came from.
    if request.referrer and "favorites" in request.referrer:
         return redirect(url_for("favorite.list_favorites"))
         
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))