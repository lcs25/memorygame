from src.helpers.stats_and_scoring import parse_results, parse_options, score_attempt

class Round:
    def __init__(self):
        self.options = {}
        self.pick = None
        self.submission = None
        self.time_elapsed = None
        self.score = None

    def set_submission(self, submission, time_elapsed):
        self.submission = submission
        self.time_elapsed = time_elapsed
        self.score_round()

    def set_sentences(self, sentences):
        for i in range(len(sentences)):
            self.options[i] = sentences[i]

    def set_pick(self, pick):
        self.pick = self.options[pick]

    def score_round(self):
        score = score_attempt(self.pick, self.submission)
        self.score = score

    def get_score(self, format=False):
        if format:
            res = parse_results(self.pick, self.submission, self.score, self.time_elapsed)
            return res, None
        return self.score, None

    def get_sentences(self, format=False):
        if format:
            return parse_options(self.options)
        return self.options

