from flask import Blueprint

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")


@comment_bp.get("/")
def list_comments():
    return {"message": "Comment controller placeholder"}
