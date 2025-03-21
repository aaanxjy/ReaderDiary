from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача", validators=[DataRequired(), Length(min=4, max=100)]
    )

    password = PasswordField(
        "Пароль", validators=[DataRequired(), Length(min=8, max=100)]
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Ім'я користувача", validators=[DataRequired(), Length(min=4, max=100)]
    )

    password = PasswordField(
        "Пароль", validators=[DataRequired(), Length(min=8, max=100)]
    )


