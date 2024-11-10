from flask_login import current_user
import requests
from flask_login import current_user
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional, ValidationError

def is_developer(form, field):
    if not current_user.is_developer:
        raise ValidationError("Only developers can add their GitHub username.")

def github_username_available(form, field):
    username = field.data
    response = requests.get(f"https://api.github.com/users/{username}", timeout=30)
    if response.status_code == 404:
        raise ValidationError("There was an error verifying your username, try again later please.")

class UserProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=100)])
    github = StringField('GitHub Username', validators=[
        DataRequired(),
        Length(min=1, max=39),
        github_username_available,
        is_developer
    ])

    orcid = StringField('ORCID', validators=[
        Optional(),
        Length(min=19, max=19, message='ORCID must have 16 numbers separated by dashes'),
        Regexp(r'^\d{4}-\d{4}-\d{4}-\d{4}$', message='Invalid ORCID format')
    ])
    affiliation = StringField('Affiliation', validators=[
        Optional(),
        Length(min=5, max=100)
    ])
    submit = SubmitField('Save profile')
