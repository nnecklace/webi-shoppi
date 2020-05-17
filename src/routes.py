from flask import render_template, request, redirect, url_for
from src.models.products.products import Product
from src.db import db
from src import app

@app.route("/")
def index():
    return render_template("index.html")

"""
Product routes
""" 

@app.route("/products")
def product_list():
    return render_template("products/main.html", products = Product.query.all())

@app.route("/products/form")
def product_form():
    return render_template("products/form.html")

@app.route("/products/<id>")
def product_edit(id):
    return render_template("products/edit.html", product = Product.query.get(id))

@app.route("/products", methods=["POST"])
def product_create():
    product = Product(
        request.form.get("name"), 
        request.form.get("price"), 
        request.form.get("quantity")
    )
    db.session().add(product)
    db.session().commit()
    return redirect(url_for("product_list"))

@app.route("/products/<id>", methods=["POST"])
def product_update(id):
    product = Product.query.get(id)

    product.name = request.form.get("name"), 
    product.price = request.form.get("price"), 
    product.quantity = request.form.get("quantity")

    db.session.commit()

    return redirect(url_for("product_list"))
