from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())

    order = db.relationship("Order",backref="order")
    cart = db.relationship("Cart",backref="cart")
    bookmarks = db.relationship("Bookmark",backref="users")

    def __repr__(self):
        return f"User >>> {self.username}"

class Bookmark(db.Model):
    __tablename__ = 'booksmarks'

    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.Text,nullable=True)
    url = db.Column(db.Text,nullable=False)
    short_url = db.Column(db.String(3),nullable=False)
    visits = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = "".join(random.choices(characters,k=3))
        link = self.query.filter_by(short_url=picked_chars).first()
        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.short_url=self.generate_short_characters()

    def __repr__(self):
        return f"Bookmark>>>{self.url}"

class Category(db.Model):
    __tablename__ = 'category'

    categoryid = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_category = db.relationship("ProductCategory",backref="productcategory")

    def __repr__(self):
        return f"Category('{self.categoryid}', '{self.category_name}')"

class Product(db.Model):
    __tablename__ = 'product'

    productid = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    regular_price = db.Column(db.DECIMAL)

    product_category = db.relationship("ProductCategory",backref="productcategory")
    cart = db.relationship("Cart",backref="cart")
    orderprod = db.relationship("OrderedProduct",backref="orderproduct")

    def __repr__(self):
        return f"Product('{self.productid}','{self.product_name}','{self.description}', '{self.image}',  '{self.quantity}', '{self.regular_price}')"

class ProductCategory(db.Model):

    __tablename__ = 'productcategory'

    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.categoryid}', '{self.productid}')"

class Cart(db.Model):

    __tablename__ = 'cart'

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Cart('{self.userid}', '{self.productid}, '{self.quantity}')"

class Order(db.Model):

    __tablename__ = 'order'

    orderid = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)

    orderprod = db.relationship("OrderedProduct",backref="orderproduct")
    sales = db.relationship("SaleTransaction",backref="salestransaction")

    def __repr__(self):
        return f"Order('{self.orderid}', '{self.order_date}','{self.total_price}','{self.userid}'')"

class OrderedProduct(db.Model):

    __tablename__ = 'orderproduct'

    ordproductid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.orderid'), nullable=False)
    productid = db.Column(db.Integer,db.ForeignKey('product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order('{self.ordproductid}', '{self.orderid}','{self.productid}','{self.quantity}')"

class SaleTransaction(db.Model):

    __tablename__ = 'salestransaction'

    transactionid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.orderid'), nullable=False)
    transaction_date = db.Column(db.DateTime,nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)

    def __repr__(self):
        return f"Order('{self.transactionid}', '{self.orderid}','{self.transactiondate}','{self.amount}')"









