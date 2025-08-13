from src.helpers.messages import SCORE
from src.helpers.constants import WORDS_PER_MINUTE, SENTENCE, SUBMISSION, OPTION
from src.config.config import c, OUTPUT_PATH, OUTPUT_FILE

def score_attempt(sentence, submission):
    distance = edit_distance_2(submission, sentence)
    slen = len(sentence)
    score = round(((slen - distance)/slen) * 100, 2)
    return '{}{}'.format(score, '%')

def parse_results(original_sentence, usr_input, score, time_elapsed):
    # score_trend_symbol, last_score_trend = get_trend(scores)
    # rate_trend_symbol, last_rate_trend = get_trend(scores)
    typing_rate = round((len(usr_input) / time_elapsed)*60, 2)
    og = '{}: {}'.format(SENTENCE, original_sentence)
    sub = '{}: {}'.format(SUBMISSION, usr_input)
    score ='{}: {}, ({}, {})'.format(SCORE, score, "", "")
    rate = '{}: {}, ({}, {})'.format(WORDS_PER_MINUTE, typing_rate, "", "")
    result = [og, sub, score, rate]
    # write_text_to_output_file(','.join(result, )
    return result

def write_text_to_output_file(text, output_folder):
    output_file = open(c(OUTPUT_PATH) + OUTPUT_FILE, "+a")
    output_file.write(text + '\n\n')

def parse_options(sentences):
    options = []
    for i in range(len(sentences)):
        option_string = "{} {}: {}".format(OPTION, i, sentences[i])
        options.append(option_string)
        options.append('\n')

    return options

def edit_distance_2(a, b):
        # Ensure 'a' is the shorter string to minimize space
    if len(a) > len(b):
        a, b = b, a

    m, n = len(a), len(b)

    prev = list(range(m + 1))  
    curr = [0] * (m + 1)

    for j in range(1, n + 1):
        curr[0] = j  
        for i in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[i] = min(
                prev[i] + 1,      
                curr[i - 1] + 1,  
                prev[i - 1] + cost  
            )
        prev, curr = curr, prev

    return prev[m]


def edit_distance(curr, target):
    if len(curr) == 0:
        return len(target)

    if len(target) == 0:
        return len(curr)

    if curr == target:
        return 0

    h_score = max(len(curr), len(target))
    i = 0

    while i < len(curr):
        j = i
        ii = target.find(curr[i], 0, len(target))
        while ii != -1:
            j = i
            jj = ii
            while j + 1 < len(curr) and jj + 1 < len(target):
                if curr[j + 1] != target[jj + 1]:
                    break
                j += 1
                jj += 1

            right_curr = curr[:i]
            right_target = target[:ii]
            left_curr = curr[j + 1:]
            left_target = target[jj + 1:]
            right_score = edit_distance(right_curr, right_target)
            left_score = edit_distance(left_curr, left_target)

            score = right_score + left_score
            if score < h_score:
                h_score = score

            ii = target.find(curr[i], ii + 1, len(target))
            if ii < jj:
                break
        i = j + 1
    return h_score
