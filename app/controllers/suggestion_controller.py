from flask import Blueprint

suggestion_bp = Blueprint("suggestion", __name__, url_prefix="/suggestions")


@suggestion_bp.get("/")
def list_suggestions():
    return {"message": "Suggestion controller placeholder"}
