from flask import render_template, request, redirect, url_for
from src.db import db
from src.models.products import Product

class ProductController:
    @staticmethod
    def index():
        return render_template("products/main.html", products = Product.query.all())

    @staticmethod
    def form():
        return render_template("products/form.html")

    @staticmethod
    def edit(id):
        return render_template("products/edit.html", product = Product.query.get(id))

    @staticmethod
    def create():
        # TODO: sanitize!!!!
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

        # TODO: sanitize!!!!
        product.name = request.form.get("name"),
        product.price = request.form.get("price"),
        product.quantity = request.form.get("quantity")

        db.session().commit()

        return redirect(url_for("product_list"))