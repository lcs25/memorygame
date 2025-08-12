# Memory Game
A simple memory game meant to improve the user's recall and typing speed.

## Features
- Flashes a set of sentences from the books in `src/data/books/`
- Scores the user's ability to recall the passage they pick.
- Tracks user score and performance in to `src/data/output/score.py`
- Meant to be played on the console, but also has a Modular IO system for flexible input/output handling,

## Configuration
All settings are defined in `src/config/config.py`:
- **`LIBRARY_PATH`** – Path to the book library (default: `src/data/books/`)
- **`OUTPUT_PATH`** – Score file path (default: `src/data/output/score.py`)
- **`CHOICE_COUNT`** – Number of sentences the user is shown per round (default: `3`)

## Setup
```bash
git clone <repo-url>
cd memorygame
pip install .