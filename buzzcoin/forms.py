from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from buzzcoin.models import User


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()], render_kw= {"placeholder": "Email"})

    password = PasswordField("Password", validators= [DataRequired()], render_kw= {"placeholder": "Password"})

    remember_me = BooleanField("Remember Me")

    submit = SubmitField("Login")


class TransactionForm(FlaskForm):

    sender = StringField("Sender", validators=[DataRequired(), Length(min = 3, max = 16)])

    receiver = StringField("Receiver", validators=[DataRequired(), Length(min = 3, max = 16)])

    amount = IntegerField("Amount", validators= [DataRequired()])

    key = StringField("Key", validators=[DataRequired()])

    send = SubmitField("Send some BuzzCoin!")

class TransactionNotLoggedInForm(FlaskForm):

    sender = StringField("Sender")

    receiver = StringField("Receiver")

    amount = IntegerField("Amount")

    key = StringField("Key")

    send = SubmitField("Sign in to start sending BuzzCoin")