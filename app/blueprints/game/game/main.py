
import pygame
import sys
from game_logic import GameLogic, questions_data # 引入遊戲邏輯和題目資料

# 初始化 Pygame
pygame.init()

# 遊戲視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gongwan Tycoon")

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# 字體設定
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# 遊戲狀態
GAME_STATE_MAIN_MENU = 0
GAME_STATE_LEVEL_SELECT = 1
GAME_STATE_GAMEPLAY = 2
GAME_STATE_RESULTS = 3

current_game_state = GAME_STATE_MAIN_MENU

game_logic = GameLogic(questions_data) # 創建遊戲邏輯實例

# --- 輔助函數 --- #
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    if rect.collidepoint(mouse):
        pygame.draw.rect(SCREEN, active_color, rect)
        if click[0] == 1 and action is not None:
            pygame.time.delay(200) # 避免重複點擊
            action()
    else:
        pygame.draw.rect(SCREEN, inactive_color, rect)

    draw_text(text, FONT, BLACK, SCREEN, x, y)
    return rect

# --- 遊戲畫面函數 --- #
def main_menu():
    global current_game_state

    SCREEN.fill(LIGHT_BLUE)
    draw_text("Gongwan Tycoon", LARGE_FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    def start_game_action():
        global current_game_state
        current_game_state = GAME_STATE_GAMEPLAY
        game_logic.reset_game()

    def level_select_action():
        global current_game_state
        current_game_state = GAME_STATE_LEVEL_SELECT

    def quit_game_action():
        pygame.quit()
        sys.exit()

    create_button("Start Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50, GREEN, LIGHT_BLUE, start_game_action)
    create_button("Level Select", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 200, 50, BLUE, LIGHT_BLUE, level_select_action)
    create_button("Quit Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140, 200, 50, RED, LIGHT_BLUE, quit_game_action)

def level_select_menu():
    global current_game_state

    SCREEN.fill(LIGHT_BLUE)
    draw_text("Select Level", LARGE_FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    # 目前只有一個關卡，直接提供一個按鈕
    def select_level_1():
        global current_game_state
        current_game_state = GAME_STATE_GAMEPLAY
        game_logic.reset_game()

    def back_to_main_menu():
        global current_game_state
        current_game_state = GAME_STATE_MAIN_MENU

    create_button("Level 1", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50, GREEN, LIGHT_BLUE, select_level_1)
    create_button("Back to Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 200, 50, BLUE, LIGHT_BLUE, back_to_main_menu)

def gameplay_screen():
    global current_game_state

    SCREEN.fill(WHITE)

    question = game_logic.get_current_question()
    if question is None:
        current_game_state = GAME_STATE_RESULTS
        return

    draw_text(f"Score: {game_logic.current_score}", FONT, BLACK, SCREEN, SCREEN_WIDTH - 100, 30)
    draw_text(f"Question {game_logic.current_question_index + 1}/{len(game_logic.questions_data)}", FONT, BLACK, SCREEN, 100, 30)

    draw_text(question["question"], FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    option_buttons = []
    for i, option in enumerate(question["options"]):
        def make_action(index=i): # 使用閉包來捕獲i的值
            def action():
                global current_game_state
                is_correct, message = game_logic.answer_question(index)
                print(message) # 暫時輸出到控制台
                # 可以考慮在這裡顯示一個短暫的答題結果提示
                if game_logic.is_level_finished():
                    current_game_state = GAME_STATE_RESULTS
            return action

        button_rect = create_button(option, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60, 600, 50, GRAY, LIGHT_BLUE, make_action())
        option_buttons.append(button_rect)

def results_screen():
    global current_game_state

    SCREEN.fill(LIGHT_BLUE)
    results = game_logic.get_level_results()

    draw_text("Level Finished!", LARGE_FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
    draw_text(f"Final Score: {results["final_score"]}", FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 80)
    draw_text(f"Correct Answers: {results["correct_count"]}", FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 120)
    draw_text(f"Incorrect Answers: {results["incorrect_count"]}", FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 160)
    draw_text(f"Level Passed: {"Yes" if results["passed_level"] else "No"}", FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 200)
    draw_text(f"Gongwan Coins Earned: {results["gongwan_coins_earned"]}", FONT, YELLOW, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 240)

    def back_to_main_menu():
        global current_game_state
        current_game_state = GAME_STATE_MAIN_MENU

    def replay_level():
        global current_game_state
        current_game_state = GAME_STATE_GAMEPLAY
        game_logic.reset_game()

    create_button("Back to Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, 200, 50, BLUE, LIGHT_BLUE, back_to_main_menu)
    create_button("Replay Level", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220, 200, 50, GREEN, LIGHT_BLUE, replay_level)

# --- 遊戲主循環 --- #
def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_game_state == GAME_STATE_MAIN_MENU:
            main_menu()
        elif current_game_state == GAME_STATE_LEVEL_SELECT:
            level_select_menu()
        elif current_game_state == GAME_STATE_GAMEPLAY:
            gameplay_screen()
        elif current_game_state == GAME_STATE_RESULTS:
            results_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()


