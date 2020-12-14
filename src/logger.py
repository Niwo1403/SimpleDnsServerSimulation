from typing import Callable


class Logger:

    def __init__(self):
        self.log_functions: {object: Callable} = {None: print}
        self.log_buffer: {object: str} = {None: ""}
        self.log_closer: {object: Callable or None} = {None: None}

    def register_logger(self, key_obj: object = None, log_function: Callable = print, close_logger: Callable = None) -> None:
        self.log_functions[key_obj] = log_function
        self.log_buffer[key_obj] = ""
        self.log_closer[key_obj] = close_logger

    def log(self, msg: str, key_obj: object = None, flush=False) -> None:
        self.log_buffer[key_obj] += msg
        if flush:
            self.flush(key_obj)

    def flush(self, key_obj: object = None):
        log_function = self.log_functions[key_obj]
        log_msg = self.log_buffer[key_obj]
        self.log_buffer[key_obj] = ""
        log_function(log_msg)

    def close_all(self):
        self.flush_all()
        close_log: Callable
        for close_log in self.log_closer:
            if close_log is not None:
                close_log()

    def flush_all(self):
        for key_name in self.log_functions:
            self.flush(key_name)


logger = Logger()
