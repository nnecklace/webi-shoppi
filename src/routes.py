from src import app
from src.controllers.products import ProductController
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

"""
Product routes
""" 

# TODO: Check blueprint route groups

@app.route("/products")
def product_list():
    return ProductController.index()

@app.route("/products/form")
def product_form():
    return ProductController.form()

@app.route("/products/<id>")
def product_edit(id):
    return ProductController.edit(id)

@app.route("/products", methods=["POST"])
def product_create():
    return ProductController.create()

@app.route("/products/<id>", methods=["POST"])
def product_update(id):
    return ProductController.update(id)