from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/")
def admin_index():
    return {"message": "Admin controller placeholder"}
