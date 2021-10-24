from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from buzzcoin.models import User


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators= [DataRequired(), Email()], render_kw= {"placeholder": "Email"})

    password = PasswordField(label="Password", validators= [DataRequired()], render_kw= {"placeholder": "Password"})

    remember_me = BooleanField(label="Remember Me")

    submit = SubmitField(label="Login")


class TransactionForm(FlaskForm):

    sender = StringField(label="Sender", validators=[DataRequired(), Length(min = 3, max = 16)])

    receiver = StringField(label="Receiver", validators=[DataRequired(), Length(min = 3, max = 16)])

    amount = IntegerField(label="Amount", validators= [DataRequired()])

    key = StringField(label="Key", validators=[DataRequired()])

    send = SubmitField(label="Send some BuzzCoin!")

class TransactionNotLoggedInForm(FlaskForm):

    sender = StringField("Sender")

    receiver = StringField("Receiver")

    amount = IntegerField("Amount")

    key = StringField("Key")

    send = SubmitField("Sign in to start sending BuzzCoin")