from flask import request, redirect, url_for
from src.controllers.base import render
from src.models.products import Product
from flask_login import current_user
from src.forms.users import ProductForm
from sqlalchemy import desc

class ProductController:
    @staticmethod
    def index():
        return render("products/main.html", products = Product.query.order_by(desc(Product.modified_at)).all())

    @staticmethod
    def create(username):
        product_form = ProductForm(request.form)
        if not product_form.validate():
            return render("users/product_form.html", product_form = product_form, session_error = "Tuotteen julkaisu epäonnistui")

        # TODO: check sanitization
        product = Product(
            product_form.name.data,
            product_form.price.data,
            product_form.quantity.data,
            current_user.id
        )

        if not product.save():
            return render("users/product_form.html", session_error = "Tuotteen julkaisu epäonnistui")

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

        if not product_form.validate():
            return render("users/product_edit.html", product_form = product_form, product = product, session_error = "Tuotteen muokkaus epäonnistui")

        product.name = product_form.name.data
        product.price = product_form.price.data
        product.quantity = product_form.quantity.data

        if not product.update():
            return render("users/product_edit.html", product_form = product_form, product = product, session_error = "Tuotteen muokkaus epäonnistui")

        return redirect(url_for("user_product_list", username = username))
    
    @staticmethod
    def delete(username, id):
        product = Product.query.get(id)

        if not product.delete():
            # TODO: Redirect back with error message
            return redirect(url_for("product_list"))

        return redirect(url_for("user_product_list", username = username))
