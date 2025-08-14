from src.BaseIO import BaseIO
import os

class ConsoleIO(BaseIO):
    def __init__(self):
        self.post_func = print
        self.request_func = input
        self.log_func = print
        super().__init__()

    def log(self, msg, err):
        return super().log(msg, err, self.log_func)

    def post(self, msg):
        return super().post(msg, self.post_func)

    def request(self, msg):
        return super().request(msg, self.request_func)

    def request_with_time(self, msg):
        return super().request_with_time(msg, self.request_func)
    
    def clear(self):
        return os.system('cls' if os.name == 'nt' else 'clear')

        

