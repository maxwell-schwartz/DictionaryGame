from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user

from app import app, db
from app.forms import LoginForm, EmptyForm, JoinGameForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Max"}
    return render_template("index.html", title="Home", user=user)


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
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign in", form=form)


@app.route("/new_game", methods=["GET", "POST"])
def create_game():
    form = EmptyForm()
    if request.method == "POST":
        return render_template("create_game.html", form=form, code="ABCD")
    return render_template("create_game.html", form=form)


@app.route("/join_game", methods=["GET", "POST"])
def join_game():
    form = JoinGameForm()
    if request.method == "POST":
        flash(f"Joined game {form.game_code.data}")
        return redirect(url_for("index"))
    return render_template("join_game.html", form=form)
