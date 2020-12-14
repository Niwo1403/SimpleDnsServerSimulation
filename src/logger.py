class Logger:
    """
    A logger, used to log text to stdout or a file.
    Text can be added by calling log(),
    but will be buffered until flush() is called.
    All methods except flush_all, require the argument key_obj,
    which can be any object, used as key to identify the logfile globally.
    Which logfile to use is set be calling register_logger()
    with the object and the filename of the log file as arguments.
    Using None as object or setting the filename to an empty string
    will result in using stdout as file.
    """

    def __init__(self):
        # None uses print()
        self.log_files: {object: str} = {None: ""}
        self.log_buffer: {object: str} = {None: ""}

    def register_logger(self,
                        key_obj: object = None,
                        log_file_name: str = "") -> None:
        """
        Adds a logger for the key object,
        which will log into the log filename.
        If the filename is empty, stdout will be used.
        :param key_obj: The object, for which the logfile should be added
        This object must be passed to the log method,
        to identify the corresponding logfile.
        :param log_file_name: The filename of the logfile.
        """
        self.log_files[key_obj] = log_file_name
        self.log_buffer[key_obj] = ""

    def log(self, text: str, key_obj: object = None, flush=False) -> None:
        """
        Adds a log entry to the buffer.
        :param text: The text to add.
        :param key_obj: The object used as key to identify the used log file.
        :param flush: True, if the current buffer should be flushed,
        after adding the text.
        """
        self.log_buffer[key_obj] += f"\n{text}"
        if flush:
            self.flush(key_obj)

    def flush(self, key_obj: object = None):
        """
        Flushed the buffered text for the key object.
        """
        log_filename = self.log_files[key_obj]
        log_text = self.log_buffer[key_obj]
        self.log_buffer[key_obj] = ""
        if log_filename == "":
            print(log_text)
        else:
            with open(log_filename, "a") as log_file:
                log_file.write(log_text)

    def flush_all(self):
        """
        Flushed all log files.
        Should be called before stopping the program,
        to ensure every log is logged.
        """
        for key_name in self.log_files:
            self.flush(key_name)


logger = Logger()
