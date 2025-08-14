from src.helpers.scoring import format_options, score_attempt, format_stats
from src.helpers.constants import ACCURACY, TYPING_RATE, SENTENCE, SUBMISSION, SCORE, WORDS_PER_MINUTE

class Round:
    def __init__(self):
        self.options = {}
        self.sentence = None
        self.submission = None
        self.time_elapsed = None
        self.score = None

    def set_submission(self, submission, time_elapsed):
        self.submission = submission
        self.time_elapsed = time_elapsed

    def set_sentences(self, sentences):
        for i in range(len(sentences)):
            self.options[i] = sentences[i]

    def get_score(self):
        if not self.score:
            return None, True
        return self.score, None

    def get_sentences(self, formatted=False):
        return self.options if not formatted else format_options(self.options)
    
    def generate_round_stats(self, formatted=True):
        accuracy_score = self.score[ACCURACY]
        typing_rate = self.score[TYPING_RATE]
        result = {SENTENCE: self.sentence, SUBMISSION: self.submission,
        SCORE: '{}{}'.format(accuracy_score, '%'),  WORDS_PER_MINUTE: typing_rate}
        return result if not formatted else format_stats(result)

    def score_round(self):
        score, self.sentence, err = score_attempt(self.options.values(), self.submission)
        if err:
            return err
        typing_rate = round((len(self.submission) / self.time_elapsed)*60, 2)
        self.score = {ACCURACY: score, TYPING_RATE: typing_rate}
        return None

    
