from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from buzzcoin.models import User

class RegistrationForm(FlaskForm):
    name = StringField('First Name', validators= [DataRequired()], render_kw={"placeholder": "Name"})

    username = StringField('Username', validators=[DataRequired(), Length(min = 3, max = 16)], 
    render_kw= {"placeholder": "Username"})

    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min = 4, max = 20)], 
    render_kw= {"placeholder": "Password"})

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo(password)], 
    render_kw= {"placeholder": "Confirm Password"})

    submit = SubmitField('Sign Up')

    def validate_username(self, username):


        # Checks if username is already taken by someone
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username already taken. Please choose a different username")
        