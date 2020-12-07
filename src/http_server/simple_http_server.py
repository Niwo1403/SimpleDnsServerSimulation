# local libraries
from request_server import RequestServer


class SimpleHttpServer:
    """
    A simplified HTTP server, which takes all incoming request
    and will return the request as well as a constant msg.
    The HTTP response header is constant.
    """

    DEFAULT_MSG_PATTERN = "HTTP/1.1 200 OK\r\n\r\nRequest\n{}\n\nMsg:\n{}"

    @staticmethod
    def _log_request(request: str) -> None:
        print(request)

    def __init__(self, msg: str, ip_address: str, port: int = 80):
        self.msg = msg
        self.server = RequestServer(ip_address, port, self.handle_request, use_udp=False)

    def handle_request(self, request: str) -> str:
        """
        Used to handle an incoming HTTP request.
        """
        self._log_request(request)
        return self._create_answer(request)

    def _create_answer(self, request: str) -> str:
        return SimpleHttpServer.DEFAULT_MSG_PATTERN.format(request, self.msg)

    def run(self) -> None:
        """
        Runs the http socket in background.
        """
        print("Starting", self.msg)
        self.server.open_socket()
        self.server.run()
        print("----------")

    def stop_listening(self) -> None:
        """
        Stops listening for requests.
        The socket won't be removed.
        """
        self.server.stop_listening()
