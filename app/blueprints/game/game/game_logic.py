
class GameLogic:
    def __init__(self, questions_data):
        self.questions_data = questions_data
        self.current_score = 0
        self.correct_answers_count = 0
        self.incorrect_answers_count = 0
        self.current_question_index = 0
        self.gongwan_coins = 0

    def get_current_question(self):
        if self.current_question_index < len(self.questions_data):
            return self.questions_data[self.current_question_index]
        return None

    def answer_question(self, selected_option_index):
        question = self.get_current_question()
        if question is None:
            return False, "No more questions."

        is_correct = (selected_option_index == question["answer"])

        if is_correct:
            self.current_score += question["score_correct"]
            self.correct_answers_count += 1
            result_message = "Correct!"
        else:
            self.current_score += question["score_wrong"]
            self.incorrect_answers_count += 1
            result_message = f"Wrong! The correct answer was: {question["options"][question["answer"]]}"
        
        self.current_question_index += 1
        return is_correct, result_message

    def is_level_finished(self):
        return self.current_question_index >= len(self.questions_data)

    def get_level_results(self):
        # 通關判定：假設答對題數大於總題數的一半則通關
        passed = self.correct_answers_count > (len(self.questions_data) / 2)
        
        # 貢丸獎勵：每答對一題獲得10個貢丸幣，分數越高貢丸幣越多
        self.gongwan_coins = self.correct_answers_count * 10 + max(0, self.current_score // 10)

        return {
            "final_score": self.current_score,
            "correct_count": self.correct_answers_count,
            "incorrect_count": self.incorrect_answers_count,
            "passed_level": passed,
            "gongwan_coins_earned": self.gongwan_coins
        }

    def reset_game(self):
        self.current_score = 0
        self.correct_answers_count = 0
        self.incorrect_answers_count = 0
        self.current_question_index = 0
        self.gongwan_coins = 0

# Sample question data
questions_data = [
    {
        "question": "Who is the creator of Python?",
        "options": ["Guido van Rossum", "James Gosling", "Brendan Eich", "Bjarne Stroustrup"],
        "answer": 0,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "Which of the following is NOT a Python data type?",
        "options": ["List", "Tuple", "Dictionary", "Array"],
        "answer": 3,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "How do you write comments in Python?",
        "options": ["//", "/* */", "#", "<!-- -->"],
        "answer": 2,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "What is the output of 'print(type([]))'?",
        "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"],
        "answer": 0,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "Which keyword is used for function definition in Python?",
        "options": ["function", "def", "func", "define"],
        "answer": 1,
        "score_correct": 10,
        "score_wrong": -5
    }
]


