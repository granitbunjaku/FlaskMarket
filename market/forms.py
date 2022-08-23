from ast import Pass
import imp
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import length, Email, equal_to, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=self.username.data).first()
        if self.username.data.__len__() < 3:
            raise ValidationError("Emri i shkurt")
        if user:
            raise ValidationError('Username already exists! Please try another one!')

    def validate_email_address(self, email_to_check):
        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email already exists! Please try another one!')
        
    username = StringField(label="User Name:")
    email_address = EmailField(label="Email:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[equal_to('password1'), DataRequired()])
    submit = SubmitField(label="Submit")


class LoginForm(FlaskForm):
    email_address = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class PurchaseForm(FlaskForm):
     submit = SubmitField(label="Purchase Item")

class SellForm(FlaskForm):
    submit = SubmitField(label="Sell Item")