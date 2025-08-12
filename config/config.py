from src.helpers.constants import IO, BASE_IO, OUTPUT_PATH, LIBRARY_PATH, MAX_ATTEMPTS, CHOICE_COUNT

OUTPUT_FILE = 'score.py'
OUTPUT_FOLDER = 'src/data/output/'
BOOK_FOLDER = 'src/data/books/'

game_configs = {
    OUTPUT_PATH: OUTPUT_FOLDER + OUTPUT_FILE,
    LIBRARY_PATH: BOOK_FOLDER,
    MAX_ATTEMPTS: 3,
    CHOICE_COUNT: 3,
    IO: BASE_IO,
}

def c(key):
    return game_configs[key]