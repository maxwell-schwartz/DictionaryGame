from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.query(User).filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        user = db.session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("There is already an account associated with this email address.")


class JoinGameForm(FlaskForm):
    game_code = StringField("Game Code")
    submit = SubmitField("Join Game")


class CreateGameForm(FlaskForm):
    submit = SubmitField("Create")


class StartGameForm(FlaskForm):
    submit = SubmitField("Start Game")


class ChooseWordForm(FlaskForm):
    word_choice = StringField("Enter Word")
    submit = SubmitField("Enter")


class EnterDefForm(FlaskForm):
    definition = TextAreaField("Enter Definition", render_kw={"rows": 10, "cols": 50})
    submit = SubmitField("Enter")
