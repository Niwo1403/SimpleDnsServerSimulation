# local libraries
from http_server.simple_http_server import SimpleHttpServer


class HttpServerBatch:
    """
    A batch of HTTP servers,
    witch can be used to create, run and stop multiple HTTP servers.
    """

    def __init__(self, ip_msg_map: {str: str}, port: int = 80):
        self.http_servers = [
            SimpleHttpServer(msg, ip_address, port)
            for ip_address, msg in ip_msg_map.items()
        ]

    def run_all(self) -> None:
        for dns_server in self.http_servers:
            dns_server.run()

    def stop(self) -> None:
        for http_server in self.http_servers:
            http_server.stop_listening()
