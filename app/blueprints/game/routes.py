from flask import current_app, Blueprint

game_bp = Blueprint("auth", __name__)

@game_bp.route("/game")
def index():
    return "Hello"