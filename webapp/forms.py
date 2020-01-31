from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.model import User


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        "Запомнить меня", default=False, render_kw={"class": "form-group"}
    )
    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"},
    )
    password2 = PasswordField(
        "Повторить пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с таким именем уже существует!")

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError(
                "Пользователь с данным адрессом электронной почты уже существует!"
            )
