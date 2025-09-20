from flask import Blueprint, request, jsonify
from .ai_assistant import handle_ai_request

ai_bp = Blueprint("ai_assistant", __name__, url_prefix="/ai")

@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    text = data.get("prompt", "")
    user = data.get("user", None)

    if not text or not user:
        return jsonify({"error": "Missing 'prompt' or 'user' in request"}), 400

    result = handle_ai_request(user, text)
    return jsonify(result)
