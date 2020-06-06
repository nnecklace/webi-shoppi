from flask_wtf import FlaskForm
from wtforms import IntegerField, validators
from src.constants import get_required_msg, get_max_integer

class BalanceForm(FlaskForm):
    balance = IntegerField("Määrä", [validators.NumberRange(min=1, max=get_max_integer(), message="Virheellinen määrä minimi määrä 1 € - maksimimäärä 1073741824"), validators.InputRequired(message=get_required_msg())])

    class Meta:
        csrf = False
