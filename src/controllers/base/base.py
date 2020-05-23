from flask import render_template
from src.forms.authentication import LoginForm

# Helper render function for rendering login form on all pages
def render(view, **kwargs):
    return render_template(view, _view_data = view, login_form = LoginForm(), **kwargs)