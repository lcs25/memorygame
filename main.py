from src.Engine import GameEngine
from src.helpers.json import save_json
from src.config.config import c
from src.helpers.constants import OUTPUT_PATH
from src.helpers.scoring import edit_distance_2, edit_distance

def main():
    game = GameEngine()
    game.play()

if __name__ == '__main__':
    main()