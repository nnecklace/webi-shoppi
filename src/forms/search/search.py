from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, widgets, SelectMultipleField, BooleanField, validators
from wtforms.fields.html5 import DateField

class MultiCheckbox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SearchForm(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(max=150, message="Tuotteen nimi on liian pitkä. Maksimipituus 150 merkkiä")])
    price = IntegerField("Hinta korkeintaan", [validators.NumberRange(max=1073741824, message="Maksimihinta on 1073741824")])
    minimum = BooleanField("Halvin")
    date_start = DateField("Jälkeen", format="%Y-%m-%d")
    date_end = DateField("Ennen", format="%Y-%m-%d")
    seller = StringField("Myyjän nimi", [validators.Length(max=150, message="Myyjän tunnus on liian pitkä. Maksimipituus 150 merkkiä")])
    categories = MultiCheckbox("Kategoriat", choices=[])