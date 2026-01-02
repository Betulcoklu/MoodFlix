from flask import Blueprint

rating_bp = Blueprint("rating", __name__, url_prefix="/ratings")


@rating_bp.get("/")
def list_ratings():
    return {"message": "Rating controller placeholder"}
