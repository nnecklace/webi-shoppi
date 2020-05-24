from src.controllers.base import render
from flask import redirect, url_for
from flask_login import current_user
from src.forms.users import ProductForm

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
