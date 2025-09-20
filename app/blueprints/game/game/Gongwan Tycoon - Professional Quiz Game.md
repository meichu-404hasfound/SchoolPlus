# Gongwan Tycoon - Professional Quiz Game

## Overview

**Gongwan Tycoon** is a modern, responsive web-based quiz game built with professional design principles. Players answer multiple-choice questions to earn points and collect "Gongwan" coins as rewards. The application features a clean, approachable interface with smooth animations and interactive elements.

## Architecture & Technology Stack

### Frontend Technologies
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS custom properties (design tokens)
- **JavaScript (ES6+)**: Modular client-side logic with async/await patterns
- **Bootstrap 5.3.3**: Responsive grid system and component library
- **Bootstrap Icons**: Comprehensive icon set for UI elements
- **Google Fonts**: Professional typography (Poppins + Roboto)

### Backend Technologies
- **Python 3.11+**: Core application logic
- **Flask 3.1.2**: Lightweight web framework
- **Flask-CORS 6.0.1**: Cross-origin resource sharing support
- **Flask-SQLAlchemy 3.1.1**: Database ORM for session management
- **SQLite**: Embedded database for game sessions

### Design System
- **Color Palette**: Professional navy blue, bright school-blue, and warm accent colors
- **Typography**: Hierarchical font system with clear readability
- **Spacing**: Consistent spacing scale using design tokens
- **Animations**: Smooth transitions and micro-interactions
- **Responsive Design**: Mobile-first approach with breakpoint optimization

## Features

### Core Gameplay
- **Multiple Choice Questions**: 4-option questions with immediate feedback
- **Scoring System**: +10 points for correct answers, -5 points for incorrect answers
- **Progress Tracking**: Real-time score updates and question counters
- **Level Completion**: Pass/fail determination based on correct answer count
- **Reward System**: Gongwan coins earned based on performance

### User Interface
- **Main Menu**: Clean landing page with game branding
- **Level Selection**: Expandable system for multiple difficulty levels
- **Gameplay Screen**: Focused question display with interactive options
- **Results Screen**: Comprehensive performance summary with animations
- **Loading States**: Professional loading indicators during transitions

### Technical Features
- **RESTful API**: Clean separation between frontend and backend
- **Session Management**: Persistent game state across requests
- **Error Handling**: Graceful error recovery with user notifications
- **Accessibility**: ARIA labels, keyboard navigation, and screen reader support
- **Performance**: Optimized animations and efficient DOM manipulation

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Local Development Setup

1. **Extract the project files**:
   ```bash
   tar -xzf gongwan-quiz-game.tar.gz
   cd gongwan-quiz-game
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```

5. **Access the game**:
   Open your web browser and navigate to `http://localhost:5000`

### Troubleshooting

#### Database Permission Issues
If you encounter SQLite database errors:
- Ensure the application has write permissions in the project directory
- On Windows, avoid running from system directories (C:\Program Files)
- Move the project to your user directory (Desktop, Documents, etc.)

#### Port Already in Use
If port 5000 is occupied:
- Stop other Flask applications
- Or modify the port in `src/main.py`: `app.run(host='0.0.0.0', port=5001, debug=True)`

## Project Structure

```
gongwan-quiz-game/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── game_logic.py          # Core game logic and question management
│   ├── routes/
│   │   └── quiz.py            # API endpoints for game operations
│   ├── static/
│   │   ├── index.html         # Main application interface
│   │   ├── styles.css         # Professional styling with design tokens
│   │   └── script.js          # Client-side game logic
│   └── database/              # SQLite database files (auto-created)
├── requirements.txt           # Python dependencies
└── README.md                 # This documentation
```

## API Documentation

### Endpoints

#### `POST /api/quiz/start`
Initializes a new game session.

**Request Body**:
```json
{
  "session_id": "player_1234567890"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Game session started successfully"
}
```

#### `GET /api/quiz/question?session_id={session_id}`
Retrieves the current question for the session.

**Response**:
```json
{
  "success": true,
  "question": "Who is the creator of Python?",
  "options": ["Guido van Rossum", "James Gosling", "Brendan Eich", "Bjarne Stroustrup"],
  "question_number": 1,
  "total_questions": 5,
  "current_score": 0,
  "finished": false
}
```

#### `POST /api/quiz/answer`
Submits an answer for the current question.

**Request Body**:
```json
{
  "session_id": "player_1234567890",
  "selected_option": 0
}
```

**Response**:
```json
{
  "success": true,
  "is_correct": true,
  "message": "Correct! Guido van Rossum created Python.",
  "current_score": 10,
  "finished": false
}
```

#### `GET /api/quiz/results?session_id={session_id}`
Retrieves final game results.

**Response**:
```json
{
  "success": true,
  "results": {
    "final_score": 50,
    "correct_count": 5,
    "incorrect_count": 0,
    "passed_level": true,
    "gongwan_coins_earned": 55
  }
}
```

#### `POST /api/quiz/reset`
Resets the game session for replay.

**Request Body**:
```json
{
  "session_id": "player_1234567890"
}
```

## Customization Guide

### Adding New Questions
Edit `src/game_logic.py` and modify the `questions` list:

```python
questions = [
    {
        "question": "Your new question here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": 0  # Index of correct option (0-3)
    },
    # ... more questions
]
```

### Modifying Scoring System
In `src/game_logic.py`, adjust the scoring constants:

```python
POINTS_CORRECT = 10    # Points for correct answers
POINTS_INCORRECT = -5  # Points deducted for incorrect answers
PASS_THRESHOLD = 3     # Minimum correct answers to pass
```

### Customizing Visual Design
Modify CSS custom properties in `src/static/styles.css`:

```css
:root {
    --sp-primary: #2C3E50;        /* Primary brand color */
    --sp-secondary: #3498DB;      /* Secondary accent color */
    --sp-accent: #F39C12;         /* Highlight color */
    /* ... other design tokens */
}
```

### Adding New Levels
Extend the level selection system by:
1. Adding level data to `src/game_logic.py`
2. Updating the level selection UI in `src/static/index.html`
3. Modifying the JavaScript logic in `src/static/script.js`

## Performance Considerations

### Frontend Optimization
- **Lazy Loading**: Images and resources loaded on demand
- **CSS Animations**: Hardware-accelerated transforms for smooth performance
- **JavaScript Efficiency**: Event delegation and minimal DOM manipulation
- **Responsive Images**: Optimized assets for different screen sizes

### Backend Optimization
- **Database Indexing**: Efficient session lookup and management
- **Caching**: Static asset caching with appropriate headers
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Session Cleanup**: Automatic cleanup of expired game sessions

## Browser Compatibility

### Supported Browsers
- **Chrome**: 90+ (recommended)
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### Required Features
- ES6+ JavaScript support
- CSS Grid and Flexbox
- CSS Custom Properties
- Fetch API
- Local Storage

## Security Considerations

### Data Protection
- **No Personal Data**: Game sessions use anonymous identifiers
- **Input Validation**: All user inputs sanitized and validated
- **CORS Configuration**: Restricted cross-origin access
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy

### Best Practices
- **Session Management**: Secure session handling with automatic cleanup
- **Error Disclosure**: Limited error information exposed to clients
- **Content Security**: No inline scripts or styles for CSP compliance

## Game Instructions

1. **Main Menu**: Click "Start Game" to begin or "Level Select" to choose a specific level
2. **Gameplay**: Read each question and click on one of the four answer options
3. **Scoring**: 
   - Correct answers: +10 points
   - Incorrect answers: -5 points
4. **Level Completion**: Answer more than half the questions correctly to pass
5. **Rewards**: Earn Gongwan coins based on your performance
6. **Results**: View your final score, correct/incorrect counts, and earned coins

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement changes with proper testing
4. Update documentation as needed
5. Submit a pull request with detailed description

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use ES6+ features and consistent formatting
- **CSS**: Maintain design token consistency and responsive principles
- **HTML**: Semantic markup with accessibility considerations

## Support

For technical support, bug reports, or feature requests, please visit:
https://help.manus.im

---

**Gongwan Tycoon** - Professional quiz gaming experience with modern web technologies. 🥟

