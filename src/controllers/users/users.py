from src.controllers.base import render
from flask import redirect, url_for
from flask_login import current_user
from src.forms.users import ProductForm
from src.models.products import Product
from src.models.categories import Category
from src.models.users import User

class UserController:
    @staticmethod
    def index(username):
        return render("users/main.html")

    @staticmethod
    def __populate_categories(product_form, categories):
        product_form.categories.choices = [(cat.id, cat.name) for cat in categories]

    @staticmethod
    def __get_view_data():
        product_form = ProductForm()
        categories = Category.query.all()
        UserController.__populate_categories(product_form, categories)
        return {"product_form": product_form, "categories": categories}

    @staticmethod
    def product_form(username):
        view_data = UserController.__get_view_data()
        return render("users/product_form.html", product_form = view_data["product_form"], categories = view_data["categories"])

    @staticmethod
    def product_list(username):
        return render("users/product_list.html", products = Product.query.filter_by(user_id = current_user.id).all())

    @staticmethod
    def product_view(username, product_id):
        view_data = UserController.__get_view_data()
        product = Product.query.get(product_id)
        selected_categories = list(map(lambda cat: int(cat.id), product.categories))

        return render("users/product_edit.html",
                       product_form = view_data["product_form"],
                       product = product,
                       selected_categories = selected_categories,
                       categories = view_data["categories"])
