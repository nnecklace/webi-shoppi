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
    def edit(username, id):
        if not username == current_user.username:
            return redirect('index')

        return render("products/edit.html", product = Product.query.get(id), product_form = ProductForm())

    @staticmethod
    def create(username):
        if not username == current_user.username:
            return redirect('index')

        product_form = ProductForm(request.form)
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
    def update(username, id):
        if not username == current_user.username:
            return redirect('index')

        product = Product.query.get(id)
        product_form = ProductForm(request.form)

        product.name = product_form.name.data
        product.price = product_form.price.data
        product.quantity = product_form.quantity.data

        if not product.update():
            return redirect(url_for("product_list"))

        return redirect(url_for("user_product_list", username = username, id = id))
