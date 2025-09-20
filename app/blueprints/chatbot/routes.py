from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from openai import OpenAI

from ..utils import get_current_user

chatbot_bp = Blueprint("chatbot", __name__)

# In-memory store: user_id -> { conv_id -> {title, messages} }
USER_CONV = {}
SEQ = 1

client = OpenAI(
    api_key="",   # ⚠️ Replace with your Groq API Key
    base_url="https://api.groq.com/openai/v1"
)

def _format_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def _next_id():
    global SEQ
    SEQ += 1
    return str(SEQ)

def _get_user_convs(user_id):
    if user_id not in USER_CONV:
        USER_CONV[user_id] = {}
    return USER_CONV[user_id]

def ask_ai_chat(prompt: str, temperature=0.7) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a school e platform. Keep answers concise, but keep a helpful/joyful tone."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

@chatbot_bp.route("/ai", methods=["GET"])
def chat():
    user = get_current_user()
    if not user:
        flash("請先登入。", "error")
        return redirect(url_for("index.login"))

    user_convs = _get_user_convs(user.account)

    chat_id = request.args.get("chat_id")
    q = request.args.get("q", "").strip().lower()

    conversations = []
    for cid, c in user_convs.items():
        if not q or q in c["title"].lower():
            conversations.append({"id": cid, "title": c["title"]})

    # pick a default conversation if none selected
    if not chat_id and conversations:
        chat_id = conversations[0]["id"]

    messages = user_convs.get(chat_id, {}).get("messages", []) if chat_id else []

    return render_template(
        "chatbot.html",
        user=user,
        conversations=sorted(conversations, key=lambda x: x["id"], reverse=True),
        messages=messages,
        chat_id=chat_id,
    )


@chatbot_bp.route("/ai/new", methods=["GET"])
def new_chat():
    user = get_current_user()
    if not user:
        flash("請先登入。", "danger")
        return redirect(url_for("index.login"))

    user_convs = _get_user_convs(user.account)
    chat_id = _next_id()
    user_convs[chat_id] = {"title": "New Conversation", "messages": []}
    return redirect(url_for("chatbot.chat", chat_id=chat_id))

# @chatbot_bp.route("/ai/send", methods=["POST"])
# def send_message():
#     user = get_current_user()
#     if not user:
#         return jsonify({"error": "unauthorized"}), 401

#     data = request.get_json(force=True)
#     chat_id = data.get("chat_id") or _next_id()
#     message = (data.get("message") or "").strip()
#     model = data.get("model") or "gpt-4o-mini"
#     temperature = float(data.get("temperature") or 0.7)

#     user_convs = _get_user_convs(user.account)
#     if chat_id not in user_convs:
#         user_convs[chat_id] = {"title": message[:40] or "Conversation", "messages": []}

#     # Save user message
#     user_msg = {
#         "id": _next_id(),
#         "role": "user",
#         "content": message,
#         "timestamp": _format_ts()
#     }
#     user_convs[chat_id]["messages"].append(user_msg)

#     if user_convs[chat_id]["title"] == "New Conversation":
#         user_convs[chat_id]["title"] = message[:40] or "Conversation"

#     # --- AI reply (stub). Replace with actual LLM API call.
#     reply_text = ask_ai_chat(message, temperature=temperature)
    
#     ai_msg = {
#         "id": _next_id(),
#         "role": "assistant",
#         "content": reply_text,
#         "timestamp": _format_ts()
#     }
#     user_convs[chat_id]["messages"].append(ai_msg)

#     return jsonify({"chat_id": chat_id, "messages": [user_msg, ai_msg]})

@chatbot_bp.route("/ai/send", methods=["POST"])
def send_message():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True)
    chat_id = data.get("chat_id") or _next_id()
    message = (data.get("message") or "").strip()
    model = data.get("model") or "gpt-4o-mini"
    temperature = float(data.get("temperature") or 0.7)

    user_convs = _get_user_convs(user.account)
    if chat_id not in user_convs:
        user_convs[chat_id] = {"title": message[:40] or "Conversation", "messages": []}

    # 儲存用戶訊息
    user_msg = {
        "id": _next_id(),
        "role": "user",
        "content": message,
        "timestamp": _format_ts()
    }
    user_convs[chat_id]["messages"].append(user_msg)

    if user_convs[chat_id]["title"] == "New Conversation":
        user_convs[chat_id]["title"] = message[:40] or "Conversation"

    # === 判斷是否要回成績或分析 ===
    lower_msg = message.lower()
    reply_text = None

    if any(kw in lower_msg for kw in ["成績", "分數", "grade", "grades"]):
        # 假的成績資料
        grades = {
            "2021 上學期": {"數學": 85, "英文": 90, "物理": 78, "化學": 88},
            "2021 下學期": {"數學": 82, "英文": 92, "物理": 80, "化學": 86},
            "2022 上學期": {"數學": 88, "英文": 89, "物理": 83, "化學": 90},
            "2022 下學期": {"數學": 91, "英文": 87, "物理": 85, "化學": 92},
            "2023 上學期": {"數學": 90, "英文": 91, "物理": 88, "化學": 89},
        }

        if "分析" in lower_msg:  # 成績分析
            # 計算平均 & 找出最好/最差科目
            all_scores = []
            subject_totals = {}
            subject_counts = {}
            for sem, subs in grades.items():
                for subj, score in subs.items():
                    all_scores.append(score)
                    subject_totals[subj] = subject_totals.get(subj, 0) + score
                    subject_counts[subj] = subject_counts.get(subj, 0) + 1

            avg_score = sum(all_scores) / len(all_scores)
            subj_avgs = {s: subject_totals[s] / subject_counts[s] for s in subject_totals}
            best_subj = max(subj_avgs, key=subj_avgs.get)
            worst_subj = min(subj_avgs, key=subj_avgs.get)

            reply_text = (
                "📊 歷年成績分析：\n"
                f"- 平均分數：約 {avg_score:.1f}\n"
                f"- 最強科目：{best_subj}（平均 {subj_avgs[best_subj]:.1f}）\n"
                f"- 最弱科目：{worst_subj}（平均 {subj_avgs[worst_subj]:.1f}）\n"
            )
        else:  # 只查成績
            reply_lines = ["以下是你的歷年成績：\n"]
            for sem, subs in grades.items():
                subs_str = "，".join([f"{subj} {score}" for subj, score in subs.items()])
                reply_lines.append(f"- {sem}：{subs_str}")
            reply_text = "\n".join(reply_lines)

    # 其他情況 → 丟給 AI
    if not reply_text:
        reply_text = ask_ai_chat(message, temperature=temperature)

    ai_msg = {
        "id": _next_id(),
        "role": "assistant",
        "content": reply_text,
        "timestamp": _format_ts()
    }
    user_convs[chat_id]["messages"].append(ai_msg)

    return jsonify({"chat_id": chat_id, "messages": [user_msg, ai_msg]})

@chatbot_bp.route("/ai/clear", methods=["POST"])
def clear_chat():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True)
    chat_id = data.get("chat_id")

    user_convs = _get_user_convs(user.account)
    if chat_id in user_convs:
        user_convs[chat_id]["messages"] = []

    return jsonify({"ok": True})
