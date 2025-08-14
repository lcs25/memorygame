from src.BaseIO import BaseIO, Message
from src.ConsoleIO import ConsoleIO
from src.Library import Library
from src.Round import Round
from src.helpers.stats_and_scoring import format_stats, percent_change
from src.helpers.constants import LIBRARY_PATH, MOVES, OUTPUT_PATH, IO, BASE_IO, EXT, NXT, PLAYER, CHOICES, READY, SUBMISSION, \
    SCORE, NEXT_ROUND, SAVE, ACCURACY, TYPING_RATE, PASSAGES_PER_ROUND, ROUNDS_PER_GAME, STATS, INVALID_ROUNDS

from src.helpers.messages import e, p
from src.helpers.json import save_json, load_json
from src.config.config import c

import numpy as np

class GameEngine:
    def __init__(self):
        self.rounds = []
        self.library = None
        self.io = None
        self.player = None
        self.load_config()
      
    def load_config(self):
        self.io = ConsoleIO() if c(IO) == BASE_IO else BaseIO()
        self.library = Library(c(LIBRARY_PATH))
        self.choice_range = ', '.join([str(d) for d in list(range(c(PASSAGES_PER_ROUND)))])
        self.round_count = c(ROUNDS_PER_GAME)
        self.player = c(PLAYER)
        self.output_path = c(OUTPUT_PATH)
        self.moves = {0: self.show_options, 
         1: self.prompt_submission, 
         2: self.show_round_stats,
         3: self.prompt_next_round,
         4: self.prompt_stats_and_save}
        self.move_id = None
    
    
    def play(self, round_data):
        curr_move = self.update_move()
        curr_func = MOVES[curr_move]
        res, err = curr_func(round_data)
        if err:
            msg = Message(txt=e(MOVES.index(curr_move)))
            error_msg = {"m": msg, "e": err}
            return error_msg
        return  res
    
    def update_move(self, data):
        if self.move_id == None:
            self.move_id = 0
        
        curr = self.move_id 
        if curr == MOVES.index(SAVE):
            self.move_id = None
            return curr
        self.move_id  += 1
        if self.move_id == MOVES.index(SAVE):
            if len(self.rounds) < (self.round_count):
                self.move_id = 0
        return curr

    def start(self):
        ext = False
        count = 0
        while not ext == EXT and len(self.rounds) < (self.round_count):
            self.play()
            err = self.prompt_submission(self.curr_round)
            if err:
                msg = Message(txt=e(SUBMISSION))
                self.io.log(msg, err)
                continue

            self.io.clear()
            err = self.show_round_stats(self.curr_round)
            if err:
                msg = Message(txt=e(SCORE))
                self.io.log(err, msg)
                return True

            if count < self.round_count:
                ext, err = self.prompt_next_round()
                if err:
                    msg = Message(txt=e(NXT))
                    self.io.log(msg, err)
                    return True
        
        if self.round_count > 1:
            self.io.clear()
            err = self.show_game_stats()
            if err:
                msg = Message(txt=e(STATS))
                self.io.log(err, msg)
                return True
            
        return False
    
    def prompt_stats_and_save(self, data):
        res = self.generate_game_stats(True)
        msg = Message(txt=res)
        msg = Message(txt=p(SAVE))
        return msg, err
    
    def process_save(self, data):
        return '', None

    def show_options(self):
        curr_round = self.generate_round()
        r_sentences = self.library.get_random_sentences(c(PASSAGES_PER_ROUND))
        curr_round.set_sentences(r_sentences)
        msg = Message(round_indicator=self.generate_round_indicator(), txt=curr_round.get_sentences(True))
        msg = Message(round_indicator=self.generate_round_indicator(), txt=(p(READY)))
        return msg, None
    
    def clear(self, data):
        return 'clear', None

    def show_round_stats(self, data):
        curr_round = self.get_round()
        stats = curr_round.generate_round_stats()
        msg = Message(round_indicator=self.generate_round_indicator(), txt=stats)
        return msg, None

    def prompt_submission(self, data):
        msg = Message(round_indicator=self.generate_round_indicator(),txt=p(SUBMISSION))
        return msg, None

    def process_submission(self, data):
        submission, time_elapsed = data[USER_INPUT], data[TIME]
        if err:
            return err
        curr_round = self.get_round()
        curr_round.set_submission(submission, time_elapsed)
        err = curr_round.score_round()
        return '', err

    def prompt_next_round(self, data):
        msg = Message(round_indicator=self.generate_round_indicator(),txt=p(NEXT_ROUND))
        return msg, None
    
    def process_next_round(self, data):
        ext = data[USER_INPUT]
        if ext == 'exit':
            self.move_id = MOVES.index(SAVE)
        return '', None

    def generate_round_indicator(self):
        round_info = f"( {len(self.rounds)} / {self.round_count} ) "
        return round_info
        
    def generate_round(self):
        new_round = Round()
        self.rounds.append(new_round)
        return new_round

    def generate_game_stats(self, formatted=True):
        acc_scores, rates, invalid_rounds = [], [], 0

        for curr_round in self.rounds:
            round_score, err = curr_round.get_score()
            if err:
                invalid_rounds += 1
                continue
            acc_score  = round_score[ACCURACY]
            acc_scores.append(acc_score)
            rates.append(round_score[TYPING_RATE])

        rates = rates if rates else [-1]
        acc_scores = acc_scores if acc_scores else [-1]

        avg_rate, rate_change = np.mean(np.array(rates)), percent_change(rates)
        avg_acc, acc_change = np.mean(np.array(acc_scores)), percent_change(acc_scores)

        result = { "speed_range": (min(rates), max(rates)), "average_speed": avg_rate, "speed_trend": rate_change,
        "accuracy_range": (min(acc_scores), max(acc_scores)), "average_accurary": '{}{}'.format(avg_acc, '%'), "accurary_trend": '{}{}'.format(acc_change, '%')}
        
        if invalid_rounds > 0:
            result[INVALID_ROUNDS] = invalid_rounds

        return result if not formatted else format_stats(result)

    def save(self):
        player_file = self.output_path + self.player + '.json'
        stats = self.generate_game_stats(False)
        err = save_json(player_file, stats)
        return err