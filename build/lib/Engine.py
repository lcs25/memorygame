from src.BaseIO import BaseIO
from src.ConsoleIO import ConsoleIO
from src.Library import Library
from src.Round import Round
from src.helpers.constants import LIBRARY_PATH, IO, BASE_IO, EXT, NXT, CHOICES, PICK, SUBMISSION, \
    SCORE, NEXT_ROUND, MAX_ATTEMPTS, PASSAGES_PER_ROUND, ROUNDS_PER_GAME

from src.helpers.messages import e, p, RANGE, WRONG_TYPE, INVALID_PICK

from src.config.config import c

class GameEngine:
    def __init__(self):
        self.rounds = []
        self.library = None
        self.io = None
        self.load_config()

    def load_config(self):
        self.io = ConsoleIO() if c(IO) == BASE_IO else BaseIO()
        self.library = Library(c(LIBRARY_PATH))
        self.choice_range = ', '.join([str(d) for d in list(range(c(PASSAGES_PER_ROUND)))])
        self.round_count = c(ROUNDS_PER_GAME)

    def play(self):
        ext = False
        count = 0
        while not ext == EXT and count < (self.round_count):
            count += 1
            curr_round = Round()
            err = self.show_options(curr_round)
            if err:
                msg = e(CHOICES)
                self.io.log(msg, err)
                return True

            pick, err = self.prompt_choice(True)
            curr_round.set_pick(pick)
            if err:
                msg = e(PICK)
                self.io.log(msg, err)
                return True

            err = self.prompt_submission(curr_round)
            if err:
                msg = e(SUBMISSION)
                self.io.log(msg, err)
                return True

            err = self.show_score(curr_round)
            if err:
                msg = e(SCORE)
                self.io.log(err, msg)
                return True

            ext, err = self.prompt_next_round()
            if err:
                msg = e(NXT)
                self.io.log(msg, err)
                return True
        return False

    def show_options(self, round):
        sentences = self.library.get_random_sentences()
        round.set_sentences(sentences)
        self.io.post(round.get_sentences(True))
        return False

    def show_error(self, error_msg):
        self.io.log(error_msg)

    def show_score(self, round):
        score, err = round.get_score(True)
        if err:
            return err
        err = self.io.post(score)
        return err

    def prompt_choice(self, retry=False):
        pick, err = self.prompt_choice_helper(p(PICK))
        if err and retry:
            attempts = 1
            while err and attempts <= c(MAX_ATTEMPTS):
                attempts += 1
                pick, err = self.prompt_choice_helper(str(err) + p(INVALID_PICK))
        return pick, err

    def prompt_choice_helper(self, prompt):
        pick, err = self.io.request(prompt)
        valid_pick, err = self.validate_pick(pick)
        return valid_pick, err

    def prompt_submission(self, round):
        submission, time_elapsed, err = self.io.request_with_time(p(SUBMISSION))
        if err:
            return err
        round.set_submission(submission, time_elapsed)
        return None

    def prompt_next_round(self):
        user_input, err = self.io.request(p(NEXT_ROUND))
        return user_input, err

    def validate_pick(self, pick):
        try:
            pick = int(pick)
            if 0 <= pick < c(PASSAGES_PER_ROUND):
                return pick, None
            return None, ValueError(e(RANGE).format(pick, self.choice_range))
        except ValueError:
            res, err = None, ValueError(e(WRONG_TYPE).format(pick, self.choice_range))
            return res, err
