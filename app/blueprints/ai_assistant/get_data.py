from flask import Blueprint, request, jsonify
from ...models.user import User
from ...models.admin import Admin
from ...models.grade import Grade
from ...models.health import Health

data_bp = Blueprint("data", __name__)

@data_bp.post("/ai/get_data")
def query_data():
    data = request.get_json()
    intent = data.get("intent")
    user_info = data.get("user")   # {id(account), role}
    role = user_info.get("role", "student")

    # 學生只能查自己
    if role == "student":
        target_account = user_info["id"]
    else:
        # 老師可查任何學生
        target_account = data.get("target_id")

    # ===== 成績查詢 =====
    if intent == "get_grades":
        grades = Grade.query.filter_by(account=target_account).all()
        rows = [
            {"科目": g.subject, "分數": g.grade, "說明": g.description or ""}
            for g in grades
        ]
        return jsonify({"columns": ["科目", "分數", "說明"], "rows": rows})

    elif intent.startswith("get_") and intent.endswith("_grade"):
        subject_map = {"math": "數學", "english": "英文", "chinese": "國文", "science": "科學"}
        key = intent.replace("get_", "").replace("_grade", "")
        subject = subject_map.get(key)
        grades = Grade.query.filter_by(account=target_account, subject=subject).all()
        rows = [
            {"科目": g.subject, "分數": g.grade, "說明": g.description or ""}
            for g in grades
        ]
        return jsonify({"columns": ["科目", "分數", "說明"], "rows": rows})

    # ===== 健康資料 =====
    elif intent == "get_health_info":
        healths = Health.query.filter_by(account=target_account).all()
        rows = [
            {
                "身高": h.height,
                "體重": h.weight,
                "日期": h.date,
                "備註": h.description or ""
            }
            for h in healths
        ]
        return jsonify({"columns": ["身高", "體重", "日期", "備註"], "rows": rows})

    # ===== 聯絡資料 =====
    elif intent == "get_contacts":
        user = User.query.get(target_account)
        if user:
            contact = {
                "姓名": user.name,
                "顯示名稱": user.display_name,
                "Email": f"{user.account}@school.com"  # 這裡可依實際 schema 改
            }
            return jsonify({"columns": ["姓名", "顯示名稱", "Email"], "rows": [contact]})
        return jsonify({"columns": ["姓名", "顯示名稱", "Email"], "rows": []})

    return jsonify({"columns": [], "rows": []})
