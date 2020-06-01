from src import app
from src.controllers import ProductController, AuthenticationController, SearchController, UserController, render
from src.decorators import user_required
from flask_login import login_required

@app.route("/")
def index():
    return render("index.html")

"""
Authentication routes
"""

@app.route("/register")
def authentication_register_form():
    return AuthenticationController.register_form()

@app.route("/register", methods=["POST"])
def authentication_register():
    return AuthenticationController.register()

@app.route("/login", methods=["POST"])
def authentication_login():
    return AuthenticationController.login()

@app.route("/logout")
def authentication_logout():
    return AuthenticationController.logout()

"""
Product routes
""" 

# TODO: Check blueprint route groups

@app.route("/products")
def product_list():
    return ProductController.index()

"""
Search routes
"""
@app.route("/search")
def search_list():
    return SearchController.get()

"""
User & Product routes
"""

@app.route("/users/<username>")
@login_required
@user_required
def user_private_profile(username):
    return UserController.index(username)

@app.route("/users/<username>/products/form")
@login_required
@user_required
def user_product_form(username):
    return UserController.product_form(username)

@app.route("/users/<username>/products", methods=["POST"])
@login_required
@user_required
def user_product_publish(username):
    return ProductController.create(username)

@app.route("/users/<username>/products")
@login_required
@user_required
def user_product_list(username):
    return UserController.product_list(username)

@app.route("/users/<username>/products/<id>")
@login_required
@user_required
def user_product_view(username, id):
    return UserController.product_view(username, id)

@app.route("/users/<username>/products/<id>", methods=["POST"])
@login_required
@user_required
def user_product_edit(username, id):
    return ProductController.update_or_delete(username, id)
