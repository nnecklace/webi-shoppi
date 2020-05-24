from src.controllers.base import render
from flask import redirect, url_for
from flask_login import current_user
from src.forms.users import ProductForm
from src.models.products import Product
from src.models.users import User

class UserController:
    @staticmethod
    def index(username):
        if username == current_user.username:
            return render("users/main.html")

        return redirect(url_for("index"))

    @staticmethod
    def product_form(username):
        # TODO: create decorator and make secure
        if username == current_user.username:
            return render("users/product_form.html", product_form = ProductForm())

        return redirect(url_for("index"))

    @staticmethod
    def product_list(username):
        if username == current_user.username:
            return render("users/product_list.html", products = Product.query.join(User).filter_by(id = current_user.id).all())

        return redirect(url_for("index"))
