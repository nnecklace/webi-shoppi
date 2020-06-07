from flask import request
from src.models import Comment, Product
from flask_login import current_user
from src.controllers import render

class CommentController:
    @staticmethod
    def create(product_id):
        comment = Comment(request.form.get("comment"), product_id, current_user.id)
        if not comment.save():
            return render("products/details.html", session_error = "Kommentin lähettäminen epäonnistui", product = Product.query.get(product_id))

        return render("products/details.html", product = Product.query.get(product_id))
