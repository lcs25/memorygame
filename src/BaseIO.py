import datetime

class BaseIO:
    def __init__(self):
        pass

    def log(self, msg, err, log_function):
        log_function(msg, err)
        return None

    def post(self, text, show_func):
        try:
            if isinstance(text, list):
                for string in text:
                    show_func(string)
            else:
                show_func(text)
            return None
        except Exception as e:
            return e

    def request(self, text, input_func):
        try:
            usr_input = input_func(text)
            return usr_input, None
        except Exception as err:
            return "", err

    def request_with_time(self, text, input_func):
        try:
            start = datetime.datetime.now()
            usr_input = input_func(text)
            end = datetime.datetime.now()
            time_elapsed = (end - start).total_seconds()
            return usr_input, time_elapsed, ""
        except Exception as err:
            return "", "", err