from src.BaseIO import BaseIO

class ConsoleIO(BaseIO):
    def __init__(self):
        self.post_func = print
        self.request_func = input
        self.log_func = print
        super().__init__()

    def log(self, msg, err):
        return super().log(msg, err, self.log_func)

    def post(self, text):
        return super().post(text, self.post_func)

    def request(self, text):
        return super().request(text, self.request_func)

    def request_with_time(self, text):
        return super().request_with_time(text, self.request_func)

