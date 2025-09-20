# Gongwan Tycoon - Quiz Game

This is a quiz game developed using Pygame, featuring a main menu, level selection screen, and gameplay screen. Players earn points and "Gongwan" coins for correct answers, and lose points for incorrect ones. The game determines if a level is cleared based on the number of correct answers.

## Game Features
- **Interactive Interface**: Graphical user interface implemented with Pygame.
- **Scoring System**: Points are awarded for correct answers and deducted for incorrect ones.
- **Level Clearance**: Determined by the number of correct answers.
- **Gongwan Rewards**: Earn virtual currency "Gongwan" upon clearing a level.

## File Structure
- `main.py`: The main game program, including the game interface (Pygame) and game state management.
- `game_logic.py`: The core game logic, handling scoring, answer validation, level clearance, and reward calculation.
- `README.md`: This documentation file.

## How to Run the Game Locally

### Step 1: Install Python
Please ensure Python 3.6 or higher is installed on your computer. You can download and install it from the [official Python website](https://www.python.org/downloads/).

### Step 2: Create and Activate a Virtual Environment (Recommended)
To avoid package conflicts, it's recommended to create a virtual environment for the game:

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate  # Windows
```

### Step 3: Install Pygame
After activating the virtual environment, install the Pygame library:

```bash
pip install pygame
```

### Step 4: Download Game Files
Download `main.py` and `game_logic.py` into the same folder.

### Step 5: Run the Game
In your terminal or command prompt, navigate to the folder where you saved the game files, then execute:

```bash
python3 main.py
```

The game window will pop up, and you can start playing!

## Game Controls
- **Main Menu**: Click "Start Game" to begin, "Level Select" to choose a level, or "Quit Game" to exit.
- **Level Select Screen**: Click "Level 1" to start the game, or "Back to Main Menu" to return to the main menu.
- **Gameplay Screen**: Click on the option buttons below the question to answer.
- **Results Screen**: Displays game results. You can choose "Back to Main Menu" or "Replay Level".

## Question Data
Question data is defined in the `questions_data` variable within the `game_logic.py` file. You can modify or expand the questions as needed.

```python
questions_data = [
    {
        "question": "Who is the creator of Python?",
        "options": ["Guido van Rossum", "James Gosling", "Brendan Eich", "Bjarne Stroustrup"],
        "answer": 0,
        "score_correct": 10,
        "score_wrong": -5
    },
    # ... more questions
]
```

Enjoy the game!

