from flask_wtf import FlaskForm
from wtforms import StringField, validators
from src.constants import get_required_msg

class UserForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.InputRequired(message=get_required_msg()), validators.Length(min=4, max=150, message='Tunnus täytyy olla vähintään 4 merkkiä pitkä')])
    email = StringField("Sähköposti", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message='Sähköpostiosoite liian pitkä, maksimipituus 150 merkkiä'), validators.Email(message='Virheellinen sähköpostiosoite')])
    first_name = StringField("Etunimi", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message='Etunimesi on liian pitkä, maksimipituus 150 merkkiä')])
    last_name = StringField("Sukunimi", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message='Sukunimesi on liian pitkä, maksimipituus 150 merkkiä')])

    class Meta:
        csrf = False