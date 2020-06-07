from flask import request, flash
from src.models import Comment, Product
from flask_login import current_user
from src.controllers import render
from src.forms import CommentForm

class CommentController:
    @staticmethod
    def create(product_id):
        comment_form = CommentForm(request.form)

        if not comment_form.validate():
            return render("products/details.html", comment_open = True, comment_form = comment_form, product = Product.query.get(product_id))

        comment = Comment(comment_form.comment.data, product_id, current_user.id)

        if not comment.save():
            flash("Kommentin lähettäminen epäonnistui", "error")
            return render("products/details.html", comment_open = True, comment_form = comment_form, product = Product.query.get(product_id))

        # return back with empty form
        flash("Kommentti lisätty", "success")
        return render("products/details.html", comment_form = CommentForm(), product = Product.query.get(product_id))
