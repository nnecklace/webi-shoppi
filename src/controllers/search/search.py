from flask import request, redirect, url_for
from src.controllers import render
from src.models import Product, Category
from src.forms import SearchForm

class SearchController:
    @staticmethod
    def get():
        search_form = SearchForm(request.args)
        categories = Category.query.all()
        search_form.categories.choices = list(map(lambda cat: (cat.id, cat.name), categories))
        search_form.categories.choices.append((-1, "Kategoriton"))

        return render("search/main.html", search_form = search_form, products = Product.find_by_criteria(
                                                                                        search_form.name.data,
                                                                                        list(map(lambda id: int(id), search_form.categories.data)),
                                                                                        search_form.price.data,
                                                                                        search_form.date_start.data,
                                                                                        search_form.date_end.data,
                                                                                        search_form.seller.data))
