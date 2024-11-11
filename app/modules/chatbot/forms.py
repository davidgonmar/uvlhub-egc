from flask_wtf import FlaskForm
from wtforms import SubmitField


class ChatbotForm(FlaskForm):
    submit = SubmitField('Save chatbot')
