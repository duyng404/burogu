import os
from app import app
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, TextAreaField, StringField
from wtforms.validators import Required

class AuthForm(FlaskForm):
    password = PasswordField('Password',validators=[Required()], render_kw={"placeholder": "Password", "autofocus": True})
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class EditForm(FlaskForm):
    editor = TextAreaField('Go Ham.', render_kw={"placeholder": "Go Ham."})
    filepath = StringField('Path to file',validators=[Required()], render_kw={"placeholder": "Path to the .md file e.g. tech/example.md"})
    submit = SubmitField('Save')

    def __init__(self,origfilepath='',*args,**kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.origfilepath = origfilepath

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.filepath.data[-3:] != '.md' and self.filepath.data[-7:] != '.hidden':
            self.filepath.errors.append('File must end in .md')
            return False
        if self.filepath.data == self.origfilepath:
            return True
        trupath = os.path.join(app.config['CONTENT_DIR'],self.filepath.data)
        if os.path.isfile(trupath):
            self.filepath.errors.append('File already exist')
            return False
        return True
