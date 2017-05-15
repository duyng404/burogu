import os
from app import app
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, TextAreaField, StringField
from wtforms.validators import Required

class AuthForm(FlaskForm):
    password = PasswordField('Password',validators=[Required()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class EditForm(FlaskForm):
    editor = TextAreaField('Go Ham.', render_kw={"placeholder": "Go Ham."})
    submit = SubmitField('Save')

class AddForm(FlaskForm):
    editor = TextAreaField('Go Ham.', render_kw={"placeholder": "Go Ham."})
    filepath = StringField('Path to file',validators=[Required()], render_kw={"placeholder": "Path to the .md file e.g. tech/example.md"})
    submit = SubmitField('Save')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.filepath.data[-3:] != '.md':
            self.filepath.errors.append('File must end in .md')
            return False
        trupath = os.path.join(app.config['CONTENT_DIR'],self.filepath.data)
        if os.path.isfile(trupath):
            self.filepath.errors.append('File already exist')
            return False
        return True
