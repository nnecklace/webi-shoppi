from flask_wtf import FlaskForm
from wtforms import StringField

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    email = StringField("Sähköposti")
    first_name = StringField("Etunimi")
    last_name = StringField("Sukunimi")
    password = StringField("Salasana")
    password_again = StringField("Salasana uudelleen")
    class Meta:
        csrf = False 