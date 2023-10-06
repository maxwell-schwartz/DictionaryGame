import random
import string

from app.models import Game


def generate_game_code(db):
    games = db.session.query(Game).all()
    existing_codes = [game.game_code for game in games]
    letters = list(string.ascii_uppercase)

    code = ""
    for _ in range(4):
        code += random.choice(letters)

    if code in existing_codes:
        return generate_game_code(db)
    return code
