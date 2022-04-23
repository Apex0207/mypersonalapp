from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, Form, BooleanField,PasswordField,validators,validators

from wtforms.validators import DataRequired,Length,Email


class LoginForm(FlaskForm):
    username=StringField('Your email',validators=[DataRequired(),Email( )])

    pwd=PasswordField('Enter password')

    loginbtn=SubmitField("Login")

class SignupForm(FlaskForm):
    fullname=StringField('Fullname',validators=[DataRequired(message="you are required to provide your name"),Length(min=4,max=25)])

    email=StringField('Email',validators=[DataRequired(),Email(message='please provide a valid email address')])

    password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=25)])
    message=TextAreaField('Message',validators=[DataRequired(message="you are required to provide your message")])

    submit=SubmitField("Submit Form")



class ContactusForm(FlaskForm):
    fullname=StringField('Fullname',validators=[DataRequired()])

    email = StringField('Your Email')

    message = TextAreaField('Message',validators=[DataRequired()])

    btn = SubmitField('Send')

