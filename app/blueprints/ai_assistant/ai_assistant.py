from openai import OpenAI

# ===== Initialize Groq Client =====
client = OpenAI(
    api_key="gsk...",   # ⚠️ Replace with your Groq API Key
    base_url="https://api.groq.com/openai/v1"
)

# Supported intents
VALID_INTENTS = {"query_grades", "grade_analysis", "health_check", "past_exams", "site_navigation", "chat"}

# ===== Detect Intent =====
def detect_intent_ai(text: str) -> str:
    system_prompt = """You are an intent classifier.
    Please classify the user's input into one of the following intents:
    - query_grades
    - grade_analysis
    - health_check
    - past_exams
    - site_navigation
    - chat
    Only return one intent, no extra words."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        max_tokens=10,
        temperature=0
    )

    intent = response.choices[0].message.content.strip()
    if intent not in VALID_INTENTS:
        intent = "chat"
    return intent

# ===== Ask Chat AI =====
def ask_ai_chat(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Keep answers concise."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ===== Extract Subject from text =====
def extract_subject(text: str):
    subjects = {"數學": "Math", "英文": "English", "國文": "Chinese", "科學": "Science"}
    for key, val in subjects.items():
        if key in text:
            return val
    return None

# ===== Main function to handle request =====
def handle_ai_request(user, text):
    """
    user: dict with {id, role, class_id}
    text: user input string
    return: {"reply_type": ..., "intent": ...}
    """

    intent = detect_intent_ai(text)

    if intent == "query_grades":
        subject = extract_subject(text)
        if subject:
            return {"reply_type": "action", "intent": f"get_{subject.lower()}_grade"}
        else:
            return {"reply_type": "action", "intent": "get_grades"}

    elif intent == "grade_analysis":
        return {"reply_type": "action", "intent": "analyze_grades"}

    elif intent == "health_check":
        return {"reply_type": "action", "intent": "get_health_info"}

    elif intent == "past_exams":
        return {"reply_type": "action", "intent": "get_past_exams"}

    elif intent == "site_navigation":
        # Only return the action keyword, not the URL
        if "activities" in text.lower():
            return {"reply_type": "action", "intent": "go_activities"}
        elif "issues" in text.lower():
            return {"reply_type": "action", "intent": "go_issues"}
        elif "grades" in text.lower():
            return {"reply_type": "action", "intent": "go_grades"}
        else:
            # Fallback → chat
            return {"reply_type": "text", "intent": ask_ai_chat(text)}

    elif intent == "chat":
        reply = ask_ai_chat(text)
        return {"reply_type": "text", "intent": reply}

    else:
        return {"reply_type": "text", "intent": ask_ai_chat(text)}
