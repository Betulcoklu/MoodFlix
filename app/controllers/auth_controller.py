from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/")
def auth_index():
    return {"message": "Auth controller placeholder"}
