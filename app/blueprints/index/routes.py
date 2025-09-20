from flask import current_app, Blueprint

index_bp = Blueprint("auth", __name__)

@index_bp.route("/")
def index():
    return "Hello"