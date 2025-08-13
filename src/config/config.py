from src.helpers.constants import IO, BASE_IO, OUTPUT_PATH, LIBRARY_PATH, MAX_ATTEMPTS, PASSAGES_PER_ROUND, PASSAGE_MIN_LENGTH, ROUNDS_PER_GAME 

OUTPUT_FILE = 'score.py'
OUTPUT_FOLDER = 'src/data/output/'
BOOK_FOLDER = 'src/data/books/'

game_configs = {
    OUTPUT_PATH: OUTPUT_FOLDER + OUTPUT_FILE,
    LIBRARY_PATH: BOOK_FOLDER,
    MAX_ATTEMPTS: 3,
    PASSAGES_PER_ROUND: 3,
    PASSAGE_MIN_LENGTH: 40,
    ROUNDS_PER_GAME: 5,
    IO: BASE_IO,
}

def c(key):
    return game_configs[key]