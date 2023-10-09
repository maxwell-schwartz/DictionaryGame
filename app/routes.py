import json

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from app import app, db
from app.forms import LoginForm, CreateGameForm, JoinGameForm, RegistrationForm, StartGameForm, ChooseWordForm
from app.models import User, Game, GameStateEnum
from app.util.game_util import create_new_game, join_existing_game, get_game_data


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            return redirect(url_for("index"))
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/new_game", methods=["GET", "POST"])
@login_required
def create_game():
    form = CreateGameForm()
    if request.method == "POST":
        code = create_new_game(current_user.get_id())
        return redirect(url_for("waiting_room", code=code))
    return render_template("create_game.html", form=form)


@app.route("/join_game", methods=["GET", "POST"])
def join_game():
    form = JoinGameForm()
    if request.method == "POST":
        joined_game, error_message = join_existing_game(current_user.get_id(), form.game_code.data)
        if not joined_game:
            flash(error_message)
        else:
            return redirect(url_for("waiting_room", code=form.game_code.data))
    return render_template("join_game.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/waiting_room/<code>", methods=["GET", "POST"])
def waiting_room(code):
    form = StartGameForm()
    game_data = get_game_data(current_user.get_id(), code)
    game = game_data.get("game")
    if request.method == "POST":
        game.game_state = GameStateEnum(1)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("word_choice", code=code))
    started = game.game_state == GameStateEnum(1)
    return render_template(
        "waiting_room.html",
        code=code,
        form=form,
        host=game_data["host"],
        user_is_host=game_data["user_is_host"],
        players=game_data["players"],
        started=started,
    )


@app.route("/word_choice/<code>", methods=["GET", "POST"])
def word_choice(code):
    form = ChooseWordForm()
    game_data = get_game_data(current_user.get_id(), code)
    return render_template("word_choice.html", form=form, user_is_host=game_data["user_is_host"])
