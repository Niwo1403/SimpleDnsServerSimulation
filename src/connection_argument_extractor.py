import re


def scan_pattern(pattern, argument):
    matched_str = None
    match = re.match(pattern, argument)
    if match is not None:
        matched_str = match.group(0)
    return matched_str


class ConnectionArgumentExtractor:
    """
    Extracts the ip address and port from a list of arguments.
    To identify the ip address and port regular expressions were used.
    The first found match will be used.
    """

    IP_PATTERN = r"^(\d{1,3}\.){3}\d{1,3}$"
    PORT_PATTERN = r"^\d{1,4}$"

    def __init__(self, argv, default_port=53):
        self.argv = argv
        self.ip_address = None
        self.port = default_port

    def get_arguments(self):
        """
        Get the connection information from the argv, which was set initially.
        The first match of an ip address will be used as ip address,
        while the last match of a port will be used as port.
        :return: A tuple of the ip address and the port.
        """
        for argument in self.argv:
            self._process_argument(argument)
        return self.ip_address, self.port

    def _process_argument(self, argument):
        self.ip_address = self.ip_address or scan_pattern(ConnectionArgumentExtractor.IP_PATTERN, argument)
        self.port = scan_pattern(ConnectionArgumentExtractor.PORT_PATTERN, argument) or self.port