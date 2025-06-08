from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, DateTimeField, TextAreaField, FileField
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')

class VideoUploadForm(FlaskForm):
    title = StringField("Enter title", [validators.DataRequired()])
    date = DateTimeField("Date", [validators.DataRequired()], default=datetime.now())
    body = TextAreaField("Enter the caption", [validators.DataRequired()])
    video = FileField("select video", [validators.DataRequired()])
    submit = SubmitField("Update", [validators.DataRequired()])
