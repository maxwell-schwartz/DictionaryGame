import json

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from app import app, db
from app.forms import LoginForm, CreateGameForm, JoinGameForm, RegistrationForm, StartGameForm
from app.models import User, Game, GameStateEnum
from app.util.code import generate_game_code
from app.util.game_util import create_new_game, join_existing_game


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
        joined_game = join_existing_game(current_user.get_id(), form.game_code.data)
        if not joined_game:
            flash("The game code you entered does not exist.")
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
    game = db.session.query(Game).filter_by(game_code=code).one()
    host = db.session.query(User).get(game.game_master).username
    user_is_host = current_user.get_id() == str(game.game_master)
    players = json.loads(game.players)
    return render_template(
        "waiting_room.html",
        code=code,
        form=form,
        host=host,
        user_is_host=user_is_host,
        players=players
    )
