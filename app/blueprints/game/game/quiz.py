from flask import Blueprint, request, jsonify, session
from src.game_logic import GameLogic, questions_data

quiz_bp = Blueprint('quiz', __name__)

# 在記憶體中儲存遊戲狀態（實際應用中可能需要使用資料庫或 Redis）
game_sessions = {}

@quiz_bp.route('/start', methods=['POST'])
def start_game():
    """開始新遊戲"""
    try:
        # 生成簡單的 session ID（實際應用中應使用更安全的方法）
        session_id = request.json.get('session_id', 'default_session')
        
        # 創建新的遊戲實例
        game_sessions[session_id] = GameLogic(questions_data)
        
        return jsonify({
            'success': True,
            'message': 'Game started successfully',
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@quiz_bp.route('/question', methods=['GET'])
def get_current_question():
    """獲取當前問題"""
    try:
        session_id = request.args.get('session_id', 'default_session')
        
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'message': 'Game session not found'
            }), 404
        
        game = game_sessions[session_id]
        question = game.get_current_question()
        
        if question is None:
            return jsonify({
                'success': True,
                'finished': True,
                'message': 'No more questions'
            })
        
        return jsonify({
            'success': True,
            'finished': False,
            'question': question['question'],
            'options': question['options'],
            'current_score': game.current_score,
            'question_number': game.current_question_index + 1,
            'total_questions': len(game.questions_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@quiz_bp.route('/answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default_session')
        selected_option = data.get('selected_option')
        
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'message': 'Game session not found'
            }), 404
        
        if selected_option is None:
            return jsonify({
                'success': False,
                'message': 'No option selected'
            }), 400
        
        game = game_sessions[session_id]
        is_correct, message = game.answer_question(selected_option)
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'message': message,
            'current_score': game.current_score,
            'finished': game.is_level_finished()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@quiz_bp.route('/results', methods=['GET'])
def get_results():
    """獲取遊戲結果"""
    try:
        session_id = request.args.get('session_id', 'default_session')
        
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'message': 'Game session not found'
            }), 404
        
        game = game_sessions[session_id]
        results = game.get_level_results()
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@quiz_bp.route('/reset', methods=['POST'])
def reset_game():
    """重置遊戲"""
    try:
        session_id = request.json.get('session_id', 'default_session')
        
        if session_id not in game_sessions:
            return jsonify({
                'success': False,
                'message': 'Game session not found'
            }), 404
        
        game = game_sessions[session_id]
        game.reset_game()
        
        return jsonify({
            'success': True,
            'message': 'Game reset successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

