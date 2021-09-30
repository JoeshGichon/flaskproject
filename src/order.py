from flask import Blueprint

orders = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

@orders.get("/")
def get_categories():
    return {"orders":[]}

