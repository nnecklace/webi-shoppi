from flask import request, redirect, url_for
from src.db import db
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
    def edit(id):
        return render("products/edit.html", product = Product.query.get(id))

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
    def update(id):
        # API could be product.update(data)
        product = Product.query.get(id)

        # TODO: check sanitization
        product.name = request.form.get("name"),
        product.price = request.form.get("price"),
        product.quantity = request.form.get("quantity")

        db.session().commit()

        return redirect(url_for("product_list"))
