from ai_assistant import handle_ai_request

if __name__ == "__main__":
    # Mock user (normally you would get this from login/session)
    student = {"id": "S12345", "role": "student", "class_id": "C1"}
    teacher = {"id": "T001", "role": "teacher", "class_id": "C1"}

    test_cases = [
        (student, "我要看數學成績"),
        (student, "查全部成績"),
        (teacher, "請幫我做成績分析"),
        (student, "請幫我健康檢查"),
        (teacher, "給我歷年考題"),
        (student, "最近有什麼活動"),
        (student, "你好，可以跟我聊天嗎？")
    ]

    for user, text in test_cases:
        result = handle_ai_request(user, text)
        print(f"\n📝 Input: {text}")
        print(f"➡️ Result: {result}")
