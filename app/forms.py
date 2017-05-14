from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.validators import Required

class AuthForm(FlaskForm):
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
