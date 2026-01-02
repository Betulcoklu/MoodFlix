from flask import Blueprint

favorite_bp = Blueprint("favorite", __name__, url_prefix="/favorites")


@favorite_bp.get("/")
def list_favorites():
    return {"message": "Favorite controller placeholder"}
