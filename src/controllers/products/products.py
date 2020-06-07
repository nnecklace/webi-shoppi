from flask import request, redirect, url_for, flash
from src.controllers import render
from src.models import Product, Category, CategoryProduct, User
from flask_login import current_user
from src.forms import ProductForm, CommentForm
from sqlalchemy import desc

class ProductController:
    @staticmethod
    def index():
        return render("products/main.html", products = Product.query.order_by(desc(Product.created_at)).filter(Product.quantity > 0).all())

    @staticmethod
    def get(id):
        return render("products/details.html", comment_form = CommentForm(), product = Product.query.get(id))

    @staticmethod
    def purchase(id):
        product = Product.query.get(id)
        user = User.query.filter_by(username = current_user.username).first()

        if not user.purchase(product):
            flash("Tuotteen osto epäonnistui", "error")
            return render("products/details.html", product = product)

        flash("Tuotteen osto onnistui", "success")
        return render("products/details.html", product = product)

    @staticmethod
    def create():
        product_form = ProductForm(request.form)
        categories_products = CategoryProduct()

        view_data = ProductController.__get_view_data()
        product_form = view_data["product_form"]
        categories_list = view_data["categories"]

        if not product_form.validate():
            flash("Tuotteen julkaisu epäonnistui", "error")
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list)

        product = Product(
            product_form.name.data,
            product_form.price.data,
            product_form.quantity.data,
            current_user.id
        )

        if not product.save():
            flash("Tuotteen julkaisu epäonnistui", "error")
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list)

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            flash("Tuote julkaistu. Kategorioiden lisäyksessä tapahtui virhe", "error")
            return render("users/product_form.html",
                          product_form = product_form,
                          categories = categories_list)

        flash("Tuote julkaistu", "success")
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
            flash("Tuotteen muokkaus epäonnistui", "error")
            return render("users/product_edit.html",
                          categories = categories,
                          product_form = product_form,
                          product = product)

        if not product.update(product_form):
            flash("Tuotteen muokkaus epäonnistui", "error")
            return render("users/product_edit.html",
                          categories = categories,
                          product_form = product_form,
                          product = product)

        if not categories_products.add_product_categories(product.id, product_form.categories.data):
            flash("Tuote muokkaus onnistui. Kategorioiden lisäyksessä tapahtui virhe", "error")
            return render("users/product_form.html",
                          categories = categories,
                          product_form = product_form)

        flash("Tuote päivitetty", "success")
        return redirect(url_for("user_product_list", username = username))
    
    @staticmethod
    def delete(username, id):
        product = Product.query.get(id)

        if not product.delete():
            flash("Ilmoituksen poisto epäonnistui", "error")
            return redirect(url_for("product_list"))

        flash("Ilmoitus poistettu", "success")
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
