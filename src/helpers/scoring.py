from src.helpers.messages import e, BELOW_MIN_SCORE
from src.helpers.constants import MIN_SCORE, OPTION, ACCURACY, TYPING_RATE
from src.config.config import c, OUTPUT_PATH, OUTPUT_FILE
import numpy as np
import random
    

def format_stats(result):
    return [f'~s0s~   {key}: {result[key]} \n' for key in result]

def write_text_to_output_file(text, output_folder):
    output_file = open(c(OUTPUT_PATH) + OUTPUT_FILE, "+a")
    output_file.write(text + '\n\n')

def format_options(sentences):
    options = []
    for i in range(len(sentences)):
        rd = random.randrange(0, len(sentences))
        option_string = " \n {} \n".format(sentences[i])
        options.insert(rd, option_string)

    return options

def edit_distance_2(a, b):
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

def percent_change(lst):
    return round(((lst[-1] - lst[0])/lst[0])*100, 2)

def score_attempt(sentences, submission):
    for original in sentences:
        distance = edit_distance_2(submission, original)
        len_og = len(original)
        score = round(((len_og - distance)/len_og)*100, 2)
        if score > MIN_SCORE:
            return score, original, None

    return None, None, ValueError(e(BELOW_MIN_SCORE))
    