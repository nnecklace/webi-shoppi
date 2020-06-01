from flask import render_template
from src.forms import LoginForm

# Helper render function for rendering login form on all pages
def render(view, **kwargs):
    # TODO: Use flask make_response to get correct url for page
    return render_template(view, _view_data = view, login_form = LoginForm(), **kwargs)