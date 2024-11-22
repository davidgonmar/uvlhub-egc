from flask_wtf import FlaskForm
from wtforms import SubmitField


class FakenodoForm(FlaskForm):
    submit = SubmitField('Save fakenodo')