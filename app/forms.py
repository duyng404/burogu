from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required

class AuthForm(FlaskForm):
    password = PasswordField('Password',validators=[Required()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class EditForm(FlaskForm):
    pagedown = TextAreaField('Enter your Markdown')
    submit = SubmitField('Submit')
