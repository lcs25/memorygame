from .constants import CHOICES, PICK, SUBMISSION, SCORE, NEXT_ROUND, NXT

def p(key):
    return STEP_PROMPTS[key]

def e(key):
    try:
        return STEP_ERRORS[key]
    except KeyError:
        return _ERRORS[key]

def _e(key):
    return _ERRORS[key]

INVALID_PICK = 'invalid_pick'
INPUT = 'input'
ATTEMPTS = 'attempts'
GENERATION = 'generation'
RANGE = 'range'
WRONG_TYPE = 'wrong_type'

_ERRORS = {
    INPUT: 'Could not process {} - exiting.',
    ATTEMPTS:'Too many attempts - exiting.',
    GENERATION: 'Could not generate {} - exiting.',
    RANGE: 'Input is out of range, ({}). ' + 'Expected one of {}.',
    WRONG_TYPE: 'Input is of wrong type, ({}). ' + 'Excepted one of {}.'
}

STEP_ERRORS = {
    SUBMISSION: _e(INPUT).format(SUBMISSION),
    CHOICES: _e(GENERATION).format(CHOICES),
    PICK: _e(ATTEMPTS).format(PICK),
    NEXT_ROUND: _e(INPUT).format(NXT),
    SCORE: _e(GENERATION).format(SCORE)
}

STEP_PROMPTS = {
    PICK: '\nChoose option: ',
    INVALID_PICK: '\nTry again: ',
    SUBMISSION: '\nSubmission: ',
    NEXT_ROUND: "Next round?"
}



