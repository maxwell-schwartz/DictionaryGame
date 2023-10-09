import json

from app import db
from app.models import Game, GameStateEnum, User
from app.util.code import generate_game_code


def create_new_game(user_id):
    code = generate_game_code(db)
    user = db.session.query(User).get(user_id)
    user.current_game = code
    db.session.add(user)
    players = []
    game = Game(
        game_master=user_id,
        players=json.dumps(players),
        game_code=code,
        round_number=0,
        game_state=GameStateEnum(0),
    )
    db.session.add(game)
    db.session.commit()
    return code


def join_existing_game(user_id, code):
    game = db.session.query(Game).filter_by(game_code=code).one_or_none()
    if not game:
        return False, "The game code you entered does not exist."
    if game.game_state.value != 0:
        return False, "You cannot join a game already in progress."
    user = db.session.query(User).get(user_id)
    players = json.loads(game.players)
    if user.username not in players:
        players.append(user.username)
        game.players = json.dumps(players)
        db.session.add(game)
        db.session.commit()
    return True, None
