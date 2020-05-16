from flask import render_template, request, jsonify
from src.models.products.products import Product
from src.db import db
from src import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products", methods=["POST"])
def product_create():
    product = Product(request.form.get("name"), request.form.get("price"), request.form.get("quantity"))
    db.session().add(product)
    db.session().commit()
    return "Success"

@app.route("/products")
def product_list():
    return render_template("products/main.html")