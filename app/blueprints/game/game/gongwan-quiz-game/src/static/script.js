/**
 * Gongwan Tycoon Quiz Game - Frontend JavaScript
 * 
 * This module handles all client-side game logic, API communication,
 * and user interface interactions for the quiz game.
 * 
 * Architecture:
 * - Screen Management: Controls visibility of different game screens
 * - API Communication: RESTful communication with Flask backend
 * - Game State: Manages current game session and user progress
 * - UI Interactions: Handles user input and visual feedback
 */

// ===== GAME STATE MANAGEMENT =====
let currentScreen = 'main-menu';
let sessionId = 'player_' + Date.now();
let isAnswering = false;
let gameData = {
    currentScore: 0,
    questionNumber: 1,
    totalQuestions: 5,
    correctAnswers: 0,
    incorrectAnswers: 0
};

// ===== API CONFIGURATION =====
const API_BASE = '/api/quiz';
const API_ENDPOINTS = {
    START: `${API_BASE}/start`,
    QUESTION: `${API_BASE}/question`,
    ANSWER: `${API_BASE}/answer`,
    RESULTS: `${API_BASE}/results`,
    RESET: `${API_BASE}/reset`
};

// ===== SCREEN MANAGEMENT FUNCTIONS =====

/**
 * Shows the specified screen and hides all others
 * @param {string} screenId - The ID of the screen to show
 */
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen with fade animation
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        targetScreen.classList.add('animate-fade');
    }
    
    currentScreen = screenId;
    
    // Update navbar active states
    updateNavbarActiveStates(screenId);
}

/**
 * Updates navbar link active states based on current screen
 * @param {string} screenId - Current active screen ID
 */
function updateNavbarActiveStates(screenId) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to corresponding nav link
    const navMap = {
        'main-menu': 0,
        'level-select': 1
    };
    
    if (navMap.hasOwnProperty(screenId)) {
        const navLinks = document.querySelectorAll('.nav-link');
        if (navLinks[navMap[screenId]]) {
            navLinks[navMap[screenId]].classList.add('active');
        }
    }
}

/**
 * Navigation functions for different screens
 */
function showMainMenu() {
    showScreen('main-menu');
}

function showLevelSelect() {
    showScreen('level-select');
}

function showLoading() {
    showScreen('loading');
}

function showGameplay() {
    showScreen('gameplay');
}

function showResults() {
    showScreen('results');
}

// ===== GAME FLOW FUNCTIONS =====

/**
 * Starts a new game session
 * Initializes game state and loads first question
 */
async function startGame() {
    showLoading();
    
    try {
        // Reset game data
        gameData = {
            currentScore: 0,
            questionNumber: 1,
            totalQuestions: 5,
            correctAnswers: 0,
            incorrectAnswers: 0
        };
        
        // Start new session with backend
        const response = await fetch(API_ENDPOINTS.START, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await loadQuestion();
        } else {
            showErrorMessage('Failed to start game: ' + data.message);
            showMainMenu();
        }
    } catch (error) {
        console.error('Error starting game:', error);
        showErrorMessage('Failed to start game. Please check your connection and try again.');
        showMainMenu();
    }
}

/**
 * Selects a specific level and starts the game
 * @param {number} levelNumber - The level number to start
 */
async function selectLevel(levelNumber) {
    // For now, we only have one level, so just start the game
    await startGame();
}

/**
 * Loads the current question from the backend
 */
async function loadQuestion() {
    try {
        const response = await fetch(`${API_ENDPOINTS.QUESTION}?session_id=${sessionId}`);
        const data = await response.json();
        
        if (data.success) {
            if (data.finished) {
                await loadResults();
            } else {
                displayQuestion(data);
                showGameplay();
            }
        } else {
            showErrorMessage('Failed to load question: ' + data.message);
            showMainMenu();
        }
    } catch (error) {
        console.error('Error loading question:', error);
        showErrorMessage('Failed to load question. Please check your connection and try again.');
        showMainMenu();
    }
}

/**
 * Displays a question and its options in the UI
 * @param {Object} questionData - Question data from backend
 */
function displayQuestion(questionData) {
    // Update game progress indicators
    updateGameProgress(questionData);
    
    // Display question text
    const questionElement = document.getElementById('question-text');
    if (questionElement) {
        questionElement.textContent = questionData.question;
    }
    
    // Clear previous options and feedback
    const optionsContainer = document.getElementById('options-container');
    const feedbackContainer = document.getElementById('feedback-container');
    
    if (optionsContainer) {
        optionsContainer.innerHTML = '';
    }
    if (feedbackContainer) {
        feedbackContainer.innerHTML = '';
    }
    
    // Create option buttons with Bootstrap styling
    if (questionData.options && optionsContainer) {
        questionData.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'btn btn-outline-primary btn-lg w-100 text-start option-btn';
            button.textContent = option;
            button.onclick = () => submitAnswer(index);
            
            // Add hover effects
            button.addEventListener('mouseenter', function() {
                this.classList.add('hover-lift');
            });
            
            optionsContainer.appendChild(button);
        });
    }
    
    isAnswering = false;
}

/**
 * Updates game progress indicators (score, question counter)
 * @param {Object} questionData - Question data containing progress info
 */
function updateGameProgress(questionData) {
    const scoreElement = document.getElementById('current-score');
    const counterElement = document.getElementById('question-counter');
    
    if (scoreElement) {
        scoreElement.textContent = `Score: ${questionData.current_score}`;
    }
    
    if (counterElement) {
        counterElement.textContent = `Question ${questionData.question_number}/${questionData.total_questions}`;
    }
    
    // Update local game data
    gameData.currentScore = questionData.current_score;
    gameData.questionNumber = questionData.question_number;
    gameData.totalQuestions = questionData.total_questions;
}

/**
 * Submits an answer to the backend
 * @param {number} selectedOption - Index of the selected option
 */
async function submitAnswer(selectedOption) {
    if (isAnswering) return; // Prevent multiple submissions
    isAnswering = true;
    
    try {
        const response = await fetch(API_ENDPOINTS.ANSWER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                selected_option: selectedOption
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show visual feedback
            displayAnswerFeedback(selectedOption, data.is_correct, data.message);
            
            // Update score display
            const scoreElement = document.getElementById('current-score');
            if (scoreElement) {
                scoreElement.textContent = `Score: ${data.current_score}`;
            }
            
            // Disable all option buttons
            disableAllOptions();
            
            // Wait for user to see feedback, then proceed
            setTimeout(async () => {
                if (data.finished) {
                    await loadResults();
                } else {
                    await loadQuestion();
                }
            }, 2500); // Increased delay for better UX
            
        } else {
            showErrorMessage('Failed to submit answer: ' + data.message);
            isAnswering = false;
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
        showErrorMessage('Failed to submit answer. Please check your connection and try again.');
        isAnswering = false;
    }
}

/**
 * Displays visual feedback for the submitted answer
 * @param {number} selectedIndex - Index of selected option
 * @param {boolean} isCorrect - Whether the answer was correct
 * @param {string} message - Feedback message from backend
 */
function displayAnswerFeedback(selectedIndex, isCorrect, message) {
    // Highlight the selected option
    const optionButtons = document.querySelectorAll('.option-btn');
    if (optionButtons[selectedIndex]) {
        const selectedButton = optionButtons[selectedIndex];
        selectedButton.classList.remove('btn-outline-primary');
        
        if (isCorrect) {
            selectedButton.classList.add('correct');
            selectedButton.innerHTML = `<i class=\"bi bi-check-circle-fill me-2\"></i>${selectedButton.textContent}`;
        } else {
            selectedButton.classList.add('incorrect');
            selectedButton.innerHTML = `<i class=\"bi bi-x-circle-fill me-2\"></i>${selectedButton.textContent}`;
        }
    }
    
    // Show feedback message
    const feedbackContainer = document.getElementById('feedback-container');
    if (feedbackContainer && message) {
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = `alert ${isCorrect ? 'alert-success' : 'alert-danger'} rounded-3 shadow-sm animate-fade`;
        feedbackDiv.innerHTML = `
            <div class=\"d-flex align-items-center\">
                <i class=\"bi ${isCorrect ? 'bi-check-circle-fill' : 'bi-x-circle-fill'} me-2 fs-5\"></i>
                <strong>${message}</strong>
            </div>
        `;
        feedbackContainer.appendChild(feedbackDiv);
    }
}

/**
 * Disables all option buttons to prevent further interaction
 */
function disableAllOptions() {
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.cursor = 'not-allowed';
        btn.onclick = null;
    });
}

/**
 * Loads and displays the final game results
 */
async function loadResults() {
    showLoading();
    
    try {
        const response = await fetch(`${API_ENDPOINTS.RESULTS}?session_id=${sessionId}`);
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results);
            showResults();
        } else {
            showErrorMessage('Failed to load results: ' + data.message);
            showMainMenu();
        }
    } catch (error) {
        console.error('Error loading results:', error);
        showErrorMessage('Failed to load results. Please check your connection and try again.');
        showMainMenu();
    }
}

/**
 * Displays the final game results in the UI
 * @param {Object} results - Results data from backend
 */
function displayResults(results) {
    const resultElements = {
        'final-score': results.final_score,
        'correct-count': results.correct_count,
        'incorrect-count': results.incorrect_count,
        'level-passed': results.passed_level ? 'Yes' : 'No',
        'gongwan-coins': results.gongwan_coins_earned
    };
    
    // Update all result displays with animation
    Object.entries(resultElements).forEach(([elementId, value]) => {
        const element = document.getElementById(elementId);
        if (element) {
            // Add counting animation for numeric values
            if (typeof value === 'number') {
                animateNumber(element, 0, value, 1000);
            } else {
                element.textContent = value;
            }
        }
    });
    
    // Update results header based on pass/fail
    const resultsHeader = document.querySelector('#results .card-header');
    if (resultsHeader && results.passed_level) {
        resultsHeader.classList.remove('bg-success');
        resultsHeader.classList.add('bg-success');
        resultsHeader.innerHTML = `
            <h2 class=\"h3 mb-0 fw-bold\">
                <i class=\"bi bi-trophy-fill me-2\"></i>Congratulations! Level Passed!
            </h2>
        `;
    }
}

/**
 * Animates a number from start to end value
 * @param {HTMLElement} element - Element to animate
 * @param {number} start - Starting number
 * @param {number} end - Ending number
 * @param {number} duration - Animation duration in ms
 */
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.round(start + (end - start) * easeOut);
        
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

/**
 * Resets the current game and starts over
 */
async function replayLevel() {
    showLoading();
    
    try {
        const response = await fetch(API_ENDPOINTS.RESET, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await loadQuestion();
        } else {
            showErrorMessage('Failed to reset game: ' + data.message);
            showMainMenu();
        }
    } catch (error) {
        console.error('Error resetting game:', error);
        showErrorMessage('Failed to reset game. Please check your connection and try again.');
        showMainMenu();
    }
}

/**
 * Quits the current game and returns to main menu
 */
function quitGame() {
    if (currentScreen === 'main-menu') {
        // If already on main menu, show confirmation to close
        if (confirm('Are you sure you want to quit Gongwan Tycoon?')) {
            window.close();
        }
    } else {
        // If in game, confirm quit to main menu
        if (confirm('Are you sure you want to quit the current game?')) {
            showMainMenu();
        }
    }
}

// ===== UTILITY FUNCTIONS =====

/**
 * Shows an error message to the user
 * @param {string} message - Error message to display
 */
function showErrorMessage(message) {
    // Create and show Bootstrap toast for error messages
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-danger border-0';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class=\"d-flex\">
            <div class=\"toast-body\">
                <i class=\"bi bi-exclamation-triangle-fill me-2\"></i>${message}
            </div>
            <button type=\"button\" class=\"btn-close btn-close-white me-2 m-auto\" data-bs-dismiss=\"toast\" aria-label=\"Close\"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Gets or creates the toast container for notifications
 * @returns {HTMLElement} Toast container element
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

// ===== INITIALIZATION =====

/**
 * Initialize the game when the DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Show main menu by default
    showMainMenu();
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(event) {
        // ESC key returns to main menu
        if (event.key === 'Escape' && currentScreen !== 'main-menu') {
            quitGame();
        }
        
        // Number keys for option selection during gameplay
        if (currentScreen === 'gameplay' && !isAnswering) {
            const num = parseInt(event.key);
            if (num >= 1 && num <= 4) {
                const optionButtons = document.querySelectorAll('.option-btn');
                if (optionButtons[num - 1]) {
                    optionButtons[num - 1].click();
                }
            }
        }
    });
    
    // Add accessibility improvements
    addAccessibilityFeatures();
    
    console.log('Gongwan Tycoon Quiz Game initialized successfully');
});

/**
 * Adds accessibility features for better user experience
 */
function addAccessibilityFeatures() {
    // Add focus management for screen transitions
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => {
        screen.addEventListener('transitionend', function() {
            if (this.classList.contains('active')) {
                // Focus first interactive element when screen becomes active
                const firstButton = this.querySelector('button, .btn, input, select, textarea');
                if (firstButton) {
                    firstButton.focus();
                }
            }
        });
    });
    
    // Add ARIA labels for better screen reader support
    const optionsContainer = document.getElementById('options-container');
    if (optionsContainer) {
        optionsContainer.setAttribute('role', 'group');
        optionsContainer.setAttribute('aria-label', 'Answer options');
    }
}

