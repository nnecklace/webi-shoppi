from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, widgets, SelectMultipleField
from src.constants import get_required_msg, get_max_integer

class MultiCheckbox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ProductForm(FlaskForm):
    name = StringField("Nimi", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message="Tuotteen nimi on liian pitkä. Maksimipituus 150.")])
    price = IntegerField("Hinta (€)", [validators.InputRequired(message=get_required_msg()), validators.NumberRange(min=1, max=get_max_integer(), message="Minimihinta on 1 € ja maksimihinta on " + str(get_max_integer()))])
    quantity = IntegerField("Kpl määrä", [validators.NumberRange(min=1, max=get_max_integer(), message="Kpl määrä täytyy olla vähintään yksi (1) ja saa maksimissaan olla " + str(get_max_integer()))])
    categories = MultiCheckbox("Label", choices=[])
    
    class Meta:
        csrf = False
