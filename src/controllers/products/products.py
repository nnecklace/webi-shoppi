from flask import request, redirect, url_for
from src.db import db
from src.controllers.base import render
from src.models.products import Product

class ProductController:
    @staticmethod
    def index():
        return render("products/main.html", products = Product.query.all())

    @staticmethod
    def form():
        return render("products/form.html")

    @staticmethod
    def edit(id):
        return render("products/edit.html", product = Product.query.get(id))

    @staticmethod
    def create():
        # TODO: check sanitization
        product = Product(
            request.form.get("name"),
            request.form.get("price"),
            request.form.get("quantity")
        )
        # TODO: Move to product model
        # API could be e.g. product.save()
        db.session().add(product)
        db.session().commit()
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
