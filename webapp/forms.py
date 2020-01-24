from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.model import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        "Remember me", default=False, render_kw={"class": "form-group"}
    )
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"class": "form-control"},
    )
    password2 = PasswordField(
        "Re-enter password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError("User with the same username already exists!")

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError("User with the same email already exists!")
