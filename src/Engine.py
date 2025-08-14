from src.BaseIO import BaseIO, Message
from src.ConsoleIO import ConsoleIO
from src.Library import Library
from src.Round import Round
from src.helpers.scoring import format_stats, percent_change
from src.helpers.constants import LIBRARY_PATH, OUTPUT_PATH, IO, BASE_IO, EXT, NXT, PLAYER, CHOICES, READY, SUBMISSION, \
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
        
    def play(self):
        ext = False
        count = 0
        while not ext == EXT and count < (self.round_count):
            count += 1
            curr_round = self.generate_round()

            err = self.show_options(curr_round)
            if err:
                print(err)
                msg = Message(txt=e(CHOICES))
                self.io.log(msg, err)
                return True

            self.io.clear()
            err = self.prompt_submission(curr_round)
            if err:
                msg = Message(txt=e(SUBMISSION))
                self.io.log(msg, err)
                continue

            self.io.clear()
            err = self.show_round_stats(curr_round)
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
    
    def show_game_stats(self):
        res = self.generate_game_stats(True)
        msg = Message(txt=res)
        err = self.io.post(msg)
        if err:
            return err
        msg = Message(txt=p(SAVE))
        save, err = self.io.request(msg)
        if err:
            return err
        if save == '':
            return self.save()
        return err

    def show_options(self, curr_round):
        r_sentences = self.library.get_random_sentences(c(PASSAGES_PER_ROUND))
        curr_round.set_sentences(r_sentences)
        msg = Message(round_indicator=self.generate_round_indicator(), txt=curr_round.get_sentences(True))
        err = self.io.post(msg)
        if err:
            return err
        msg = Message(round_indicator=self.generate_round_indicator(), txt=(p(READY)))
        _, err = self.io.request(msg)
        return err

    def show_round_stats(self, curr_round):
        stats = curr_round.generate_round_stats()
        msg = Message(round_indicator=self.generate_round_indicator(), txt=stats)
        err = self.io.post(msg)
        return err

    def prompt_choice_helper(self, choice_prompt):
        msg = Message(round_indicator=self.generate_round_indicator(),txt=choice_prompt)
        pick, err = self.io.request(msg)
        valid_pick, err = self.validate_pick(pick)
        return valid_pick, err

    def prompt_submission(self, curr_round):
        msg = Message(round_indicator=self.generate_round_indicator(),txt=p(SUBMISSION))
        submission, time_elapsed, err = self.io.request_with_time(msg)
        if err:
            return err
        curr_round.set_submission(submission, time_elapsed)
        err = curr_round.score_round()
        return err

    def prompt_next_round(self):
        msg = Message(round_indicator=self.generate_round_indicator(),txt=p(NEXT_ROUND))
        user_input, err = self.io.request(msg)
        return user_input, err
    
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

    
            # _, err = self.prompt_choice(curr_round, True)
            # if err:
            #     msg = e(PICK)
            #     self.io.log(msg, err)
            #     return True

                # def prompt_choice(self, curr_round, retry=False):
    #     pick, err = self.prompt_choice_helper(p(PICK))
    #     if err and retry:
    #         attempts = 1
    #         while err and attempts <= c(MAX_ATTEMPTS):
    #             attempts += 1
    #             self.io.clear()
    #             pick, err = self.prompt_choice_helper(str(err) + p(INVALID_PICK))
    #     if not err:
    #         curr_round.set_pick(pick)
    #         return None, err
    #     return pick, err

        # def validate_pick(self, pick):
    #     try:
    #         pick = int(pick)
    #         if 0 <= pick < c(PASSAGES_PER_ROUND):
    #             return pick, None
    #         return None, ValueError(e(RANGE).format(pick, self.choice_range))
    #     except ValueError:
    #         res, err = None, ValueError(e(WRONG_TYPE).format(pick, self.choice_range))
    #         return res, err