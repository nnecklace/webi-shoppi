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
    def __populate_and_get_categories(product_form, request):
        categories_request = list(zip(request.form.getlist("category_id"), request.form.getlist("category_value")))
        categories_list = []

        for cat in categories_request:
            product_form.categories.choices.append(cat)
            categories_list.append(Category(id=int(cat[0]), name=cat[1]))

        return categories_list

    @staticmethod
    def create(username):
        product_form = ProductForm(request.form)
        categories_products = CategoryProduct()

        categories_list = ProductController.__populate_and_get_categories(product_form, request)

        if not product_form.validate():
            return render("users/product_form.html", product_form = product_form, categories = categories_list, session_error = "Tuotteen julkaisu epäonnistui")

        # TODO: check sanitization
        product = Product(
            product_form.name.data,
            product_form.price.data,
            product_form.quantity.data,
            current_user.id
        )

        if not product.save():
            return render("users/product_form.html", product_form = product_form, categories = categories_list, session_error = "Tuotteen julkaisu epäonnistui")

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            return render("users/product_form.html", product_form = product_form, categories = categories_list, session_error = "Tuote julkaistu. Kategorioiden lisäyksessä tapahtui virhe")

        return redirect(url_for("product_list"))

    @staticmethod
    def update_or_delete(username, id):
        if request.form.get("_method") == "DELETE":
            return ProductController.delete(username, id)

        return ProductController.update(username, id)

    @staticmethod
    def update(username, id):
        product = Product.query.get(id)
        product_form = ProductForm(request.form)
        categories_products = CategoryProduct()

        categories_list = ProductController.__populate_and_get_categories(product_form, request)

        if not product_form.validate():
            return render("users/product_edit.html", categories = categories_list, product_form = product_form, product = product, session_error = "Tuotteen muokkaus epäonnistui")

        if not product.update(product_form):
            return render("users/product_edit.html", categories = categories_list, product_form = product_form, product = product, session_error = "Tuotteen muokkaus epäonnistui")

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            return render("users/product_form.html", categories = categories_list, product_form = product_form, session_error = "Tuote muokkaus onnistui. Kategorioiden lisäyksessä tapahtui virhe")

        return redirect(url_for("user_product_list", username = username))
    
    @staticmethod
    def delete(username, id):
        product = Product.query.get(id)

        if not product.delete():
            # TODO: Redirect back with error message
            return redirect(url_for("product_list"))

        return redirect(url_for("user_product_list", username = username))
