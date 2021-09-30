from flask import Blueprint

products = Blueprint("products", __name__, url_prefix="/api/v1/products")
