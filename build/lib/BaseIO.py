import datetime
from dataclasses import dataclass

@dataclass(slots=True)
class Message:
    txt: str
    round_indicator: str = ""

class BaseIO:
    def __init__(self):
        pass

    def log(self, msg, err, log_function):
        log_function(msg, err)
        return None

    def post(self, msg, show_func):
        try:
            if isinstance(msg.txt, list):
                for string in msg.txt:
                    show_func(string)
            else:
                show_func(msg.txt)
            return None
        except Exception as err:
            return err

    def request(self, msg, input_func):
        try:
            usr_input = input_func(msg.round_indicator + msg.txt)
            return usr_input, None
        except Exception as err:
            return "", err

    def request_with_time(self, msg, input_func):
        try:
            start = datetime.datetime.now()
            usr_input = input_func(msg.round_indicator + msg.txt)
            end = datetime.datetime.now()
            time_elapsed = (end - start).total_seconds()
            return usr_input, time_elapsed, ""
        except Exception as err:
            return "", "", err

