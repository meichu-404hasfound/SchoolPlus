from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
from .ai_assistant import handle_ai_request
from ..utils import get_current_user
from ...extensions import db

ai_assistant_bp = Blueprint("ai_assistant", __name__)

@ai_assistant_bp.get("/ai/chat")
def chat_get():
    return render_template("aichat.html", respond="")

@ai_assistant_bp.post("/ai/chat")
def chat_post():
    user = get_current_user()
    prompt = request.form.get("prompt")

    if not user:
        flash("請先登入。", "error")
        return redirect(url_for("index.login"))
    
    if not prompt:
        flash("請輸入你的問題。", "error")
        return redirect(url_for("ai_assistant.chat_get"))

    result = handle_ai_request(user, prompt)
    return render_template("aichat.html", respond=result)
