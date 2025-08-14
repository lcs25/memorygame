from .constants import CHOICES, READY, SUBMISSION, SCORE, NEXT_ROUND, NXT, STATS, SAVE

def p(key):
    return STEP_PROMPTS[key]

def e(key):
    try:
        return STEP_ERRORS[key]
    except KeyError:
        return _ERRORS[key]

def _e(key):
    return _ERRORS[key]

# INVALID_PICK = 'invalid_pick'
INPUT = 'input'
ATTEMPTS = 'attempts'
GENERATION = 'generation'
RANGE = 'range'
WRONG_TYPE = 'wrong_type'
BELOW_MIN_SCORE = 'below_min_score'

_ERRORS = {
    INPUT: 'Could not process {}.',
    ATTEMPTS:'Too many attempts.',
    GENERATION: 'Could not generate {} - exiting.',
    RANGE: 'Input is out of range, ({}). ' + 'Expected one of {}.',
    WRONG_TYPE: 'Input is of wrong type, ({}). ' + 'Excepted one of {}.',
    BELOW_MIN_SCORE: 'Skipping. \n'
}

STEP_ERRORS = {
    SUBMISSION: _e(INPUT).format(SUBMISSION),
    CHOICES: _e(GENERATION).format(CHOICES),
    NEXT_ROUND: _e(INPUT).format(NXT),
    SCORE: _e(GENERATION).format(SCORE),
    STATS: _e(GENERATION).format(STATS),
}

STEP_PROMPTS = {
    READY: "\nPress 'enter' when ready to start.",
    SUBMISSION: "(Press 'enter' to skip)\nSubmission: ",
    NEXT_ROUND: "\nNext round?",
    SAVE: 'Save? (y|anything else)'
}



