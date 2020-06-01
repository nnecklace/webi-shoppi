from flask import request, redirect, url_for
from src.controllers import render
from src.models import Product, Category, CategoryProduct, User
from flask_login import current_user
from src.forms import ProductForm
from sqlalchemy import desc

class ProductController:
    @staticmethod
    def index():
        return render("products/main.html", products = Product.query.order_by(desc(Product.created_at)).filter(Product.quantity > 0).all())

    @staticmethod
    def create():
        product_form = ProductForm(request.form)
        categories_products = CategoryProduct()

        view_data = ProductController.__get_view_data()
        product_form = view_data["product_form"]
        categories_list = view_data["categories"]

        if not product_form.validate():
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list,
                          session_error = "Tuotteen julkaisu epäonnistui")

        # TODO: check sanitization
        product = Product(
            product_form.name.data,
            product_form.price.data,
            product_form.quantity.data,
            current_user.id
        )

        if not product.save():
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list,
                          session_error = "Tuotteen julkaisu epäonnistui")

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list,
                          session_error = "Tuote julkaistu. Kategorioiden lisäyksessä tapahtui virhe")

        return redirect(url_for("product_list"))

    @staticmethod
    def update_or_delete(username, id):
        if request.form.get("_method") == "DELETE":
            return ProductController.delete(username, id)

        return ProductController.update(username, id)

    @staticmethod
    def update(username, id):
        product = Product.query.get(id)
        view_data = ProductController.__get_view_data()
        categories_products = CategoryProduct()

        product_form = view_data["product_form"]
        categories = view_data["categories"]

        if not product_form.validate():
            return render("users/product_edit.html",
                          categories = categories,
                          product_form = product_form,
                          product = product,
                          session_error = "Tuotteen muokkaus epäonnistui")

        if not product.update(product_form):
            return render("users/product_edit.html",
                          categories = categories,
                          product_form = product_form,
                          product = product,
                          session_error = "Tuotteen muokkaus epäonnistui")

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            return render("users/product_form.html",
                          categories = categories,
                          product_form = product_form,
                          session_error = "Tuote muokkaus onnistui. Kategorioiden lisäyksessä tapahtui virhe")

        return redirect(url_for("user_product_list", username = username))
    
    @staticmethod
    def delete(username, id):
        product = Product.query.get(id)

        if not product.delete():
            # TODO: Redirect back with error message
            return redirect(url_for("product_list"))

        return redirect(url_for("user_product_list", username = username))

    @staticmethod
    def current_user_list():
        return render("users/product_list.html", products = Product.query.filter_by(user_id = current_user.id).all())

    @staticmethod
    def edit(product_id):
        view_data = ProductController.__get_view_data()
        product = Product.query.get(product_id)
        selected_categories = list(map(lambda cat: str(cat.id), product.categories))

        return render("users/product_edit.html",
                       product_form = view_data["product_form"],
                       product = product,
                       selected_categories = selected_categories,
                       categories = view_data["categories"])

    @staticmethod
    def form():
        view_data = ProductController.__get_view_data()
        return render("users/product_form.html", product_form = view_data["product_form"], categories = view_data["categories"])

    @staticmethod
    def __get_view_data():
        product_form = ProductForm(request.form)
        categories = Category.query.all()

        if not product_form.categories.choices:
            # flaskwtforms requires that multi checkbox widget has string values
            product_form.categories.choices = [(str(cat.id), cat.name) for cat in categories]

        return {"product_form": product_form, "categories": categories}
