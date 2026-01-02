from flask import Blueprint

movie_bp = Blueprint("movie", __name__, url_prefix="/movies")


@movie_bp.get("/")
def list_movies():
    return {"message": "Movie controller placeholder"}
