from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_developer = BooleanField('Developer')
    submit = SubmitField('Submit')
    

class SignupCodeForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Validate')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Continue')
    

class CodeForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(max=6)])
    submit = SubmitField('Validate')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Validate')