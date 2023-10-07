import enum

from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    current_game = db.Column(db.String(64))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameStateEnum(enum.Enum):
    WAITING_FOR_WORD = 1
    WAITING_FOR_DEFS = 2
    WAITING_FOR_VOTES = 3
    RESULTS = 4


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_master = db.Column(db.Integer, db.ForeignKey("user.id"))
    game_code = db.Column(db.String(64), index=True, unique=True)
    round_number = db.Column(db.Integer)
    game_state = db.Column(Enum(GameStateEnum))

    def __repr__(self):
        return f"<Game {self.game_code}>"


@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
