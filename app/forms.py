from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class JoinGameForm(FlaskForm):
    game_code = StringField("Game Code")
    submit = SubmitField("Join Game")


class EmptyForm(FlaskForm):
    submit = SubmitField('Create')
