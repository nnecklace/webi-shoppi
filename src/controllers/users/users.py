from src.controllers.base import render
from flask import redirect, url_for
from flask_login import current_user
from src.forms.users import ProductForm
from src.models.products import Product
from src.models.users import User

class UserController:
    @staticmethod
    def index(username):
        return render("users/main.html")

    @staticmethod
    def product_form(username):
        return render("users/product_form.html", product_form = ProductForm())


    @staticmethod
    def product_list(username):
        return render("users/product_list.html", products = Product.query.join(User).filter_by(id = current_user.id).all())

    @staticmethod
    def product_view(username, id):
        return render("users/product_edit.html", product_form = ProductForm(), product = Product.query.get(id))
        