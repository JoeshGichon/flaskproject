from flask import Blueprint

categories = Blueprint("categories", __name__, url_prefix="/api/v1/categories")

@categories.get("/")
def get_categories():
    return {"categories":[]}

