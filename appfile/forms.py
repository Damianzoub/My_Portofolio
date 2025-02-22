from flask_wtf import FlaskForm
from wtforms import EmailField, StringField , TextAreaField , SubmitField , PasswordField
from wtforms.validators import DataRequired , Email ,Length


class ContactForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=3,max=30)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    text_area = TextAreaField('Text Area',validators=[DataRequired()])
    submit = SubmitField('Send')

class BlogForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=5,max=35)])
    content = TextAreaField("Content",validators=[DataRequired()])
    submit = SubmitField('Submit')

class IdentifyForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")
