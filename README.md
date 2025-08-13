# Memory Game
A simple memory game meant to improve the user's recall and typing speed.

## Features
- Flashes a set of sentences from the books in `src/data/books/`
- Scores the user's ability to recall the passage they pick.
- Tracks user score and performance.
- Meant to be played on the console, but also has a Modular IO system for flexible input/output handling,

## Configuration
All configs are defined in `src/config/config.py`, 

Books:
-- Harry Potter and The Philosopher's Stone
-- The Unbearable Lightness of Being
-- The Art of Fielding
-- Pride and Prejudice

Gameplay config(s):
- PASSAGE_COUNT – Number of sentences the user is shown per round (default: 3)
- PASSAGE_LENGTH -- Length of the passages user is shown (default: min 40 chars, a decent sized sentence.)
- ROUNDS_PER_GAME -- Round many rounds the game last.

## Setup
```bash
git clone <repo-url>
cd memorygame
pip install .
python3 main.py (or python main.py)
