import re

from src.helpers.constants import COMPARISON_REGEX
from src.config.config import c, PASSAGE_MIN_LENGTH
p_min = c(PASSAGE_MIN_LENGTH)
MIN = rf"(?<=\.\s)[A-Z][a-z]{{2,}}[^.!?]{{{p_min},}}\s[a-z]+[.!?][\.\s]"

def get_all_sentences(text):
    
    sentences = re.findall(MIN, text)
    return [streamline_sentence(sentence) for sentence in sentences]

def get_text(filename):
    text = open(str(filename), "r").read()
    return get_all_sentences(text)

def get_all_comparisons(text):
    comparison_regex = COMPARISON_REGEX
    matching_strings = re.findall(comparison_regex, text)
    return matching_strings

def remove_empty_spaces(sentence):
    word_list = sentence.split(' ')
    while '' in word_list:
        word_list.remove('')
    return ' '.join(word_list)

def streamline_sentence(sentence):
    sentence = remove_empty_spaces(sentence).replace('\n', ' ')
    return sentence

