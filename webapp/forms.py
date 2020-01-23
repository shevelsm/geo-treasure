from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


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
