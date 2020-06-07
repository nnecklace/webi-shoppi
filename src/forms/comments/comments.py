from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators
from src.constants import get_required_msg

class CommentForm(FlaskForm):
    comment = TextAreaField("Kommentti", [validators.InputRequired(message=get_required_msg()), validators.Length(max=1000000000, message="Kommenttisi on liian pitkä")])

    class Meta:
        csrf = False