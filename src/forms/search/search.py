from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, widgets, SelectMultipleField
from wtforms.fields.html5 import DateField

class MultiCheckbox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SearchForm(FlaskForm):
    name = StringField("Tuotteen nimi")
    price = IntegerField("Hinta korkeintaan")
    date_start = DateField("Jälkeen", format="%Y-%m-%d")
    date_end = DateField("Ennen", format="%Y-%m-%d")
    seller = StringField("Myyjän nimi")
    categories = MultiCheckbox("Kategoriat", choices=[])