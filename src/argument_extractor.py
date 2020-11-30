import re


def scan_pattern(pattern, argument):
    matched_str = None
    match = re.match(pattern, argument)
    if match is not None:
        matched_str = match.group(0)
    return matched_str


class ArgumentExtractor:

    IP_PATTERN = r"^(\d{1,3}\.){3}\d{1,3}$"
    PORT_PATTERN = r"^\d{1,4}$"

    def __init__(self, argv, default_port=53):
        self.argv = argv
        self.ip_address = None
        self.port = default_port

    def get_arguments(self):
        for argument in self.argv:
            self._process_argument(argument)
        return self.ip_address, self.port

    def _process_argument(self, argument):
        self.ip_address = scan_pattern(ArgumentExtractor.IP_PATTERN, argument) or self.ip_address
        self.port = scan_pattern(ArgumentExtractor.PORT_PATTERN, argument) or self.port
