from sys import argv
from time import sleep

from src.connection_argument_extractor import ConnectionArgumentExtractor
from src.tcp_server import TcpServer


class SimpleDnsServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self._ensure_connection_information()
        self.server = TcpServer(self.ip_address, self.port, self.handle_request, log_requests=True)  # TODO: Deactivate logging later.

    def run(self):
        self.server.open_socket()
        self.server.run()  # will be in background
        self._run_till_interrupt()

    def handle_request(self, request):
        return f"HTTP/1.1 200 OK\r\n\r\nHI THERE!\n\nRequest:\n\n{request}"  # TODO: handle the actual request

    def _ensure_connection_information(self):
        if type(self.port) == str and self.port.isnumeric():
            self.port = int(self.port)
        assert type(self.ip_address) == str and len(self.ip_address) >= 7, "Ip address missing."
        assert type(self.port) == int, "Port must be numeric."

    def _run_till_interrupt(self):
        while True:
            try:
                sleep(60)
            except KeyboardInterrupt:  # Ctrl + C
                print("Stopped server.")
                break
        self.server.stop()


def started_as_main():
    return __name__ == "__main__"


if started_as_main():
    arg_ip, arg_port = ConnectionArgumentExtractor(argv).get_arguments()
    dns_server = SimpleDnsServer(arg_ip, arg_port)
    dns_server.run()
