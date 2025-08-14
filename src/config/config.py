from src.helpers.constants import IO, BASE_IO, OUTPUT_PATH, LIBRARY_PATH, PLAYER, MAX_ATTEMPTS, PASSAGES_PER_ROUND, PASSAGE_MIN_LENGTH, ROUNDS_PER_GAME 

OUTPUT_FILE = 'score.py'
OUTPUT_FOLDER = 'src/data/outputs/'
BOOK_FOLDER = 'src/data/books/'
PLAYER_ID = 'me'

game_configs = {
    OUTPUT_PATH: OUTPUT_FOLDER,
    PLAYER: PLAYER_ID,
    LIBRARY_PATH: BOOK_FOLDER,
    MAX_ATTEMPTS: 3,
    PASSAGES_PER_ROUND: 2,
    PASSAGE_MIN_LENGTH: 40,
    ROUNDS_PER_GAME: 2,
    IO: BASE_IO,
}


def c(key):
    return game_configs[key]