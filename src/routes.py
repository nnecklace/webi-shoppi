from src import app
from src.controllers import ProductController, AuthenticationController, SearchController, UserController, CommentController, render
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

@app.route("/products")
def product_list():
    return ProductController.index()

@app.route("/products/<id>")
def product_details(id):
    return ProductController.get(id)

@app.route("/products/<id>", methods=["POST"])
@login_required
def product_purchase(id):
    return ProductController.purchase(id)

@app.route("/products/<id>/comments", methods=["POST"])
@login_required
def product_comment(id):
    return CommentController.create(id)

"""
Search routes
"""
@app.route("/search")
def search_list():
    return SearchController.get()

"""
User & User Product routes
"""

@app.route("/users/<username>")
@login_required
@user_required
def user_private_profile(username):
    return UserController.index(username)

@app.route("/users/<username>", methods=["POST"])
@login_required
@user_required
def user_profile_update(username):
    return UserController.update(username)

@app.route("/users/<username>/balance")
@login_required
@user_required
def user_balance_form(username):
    return UserController.balance_form()

@app.route("/users/<username>/balance", methods=["POST"])
@login_required
@user_required
def user_balance_add(username):
    return UserController.add_balance(username)

@app.route("/users/<id>/delete", methods=["POST"])
@login_required
@user_required
def user_profile_delete(id):
    return UserController.delete(id)

@app.route("/users/<username>/password", methods=["POST"])
@login_required
@user_required
def user_change_password(username):
    return UserController.change_password(username)

@app.route("/users/<username>/products/form")
@login_required
@user_required
def user_product_form(username):
    return ProductController.form()

@app.route("/users/<username>/products", methods=["POST"])
@login_required
@user_required
def user_product_publish(username):
    return ProductController.create()

@app.route("/users/<username>/products")
@login_required
@user_required
def user_product_list(username):
    return ProductController.current_user_list()

@app.route("/users/<username>/products/<id>")
@login_required
@user_required
def user_product_view(username, id):
    return ProductController.edit(id)

@app.route("/users/<username>/products/<id>", methods=["POST"])
@login_required
@user_required
def user_product_edit(username, id):
    return ProductController.update_or_delete(username, id)
