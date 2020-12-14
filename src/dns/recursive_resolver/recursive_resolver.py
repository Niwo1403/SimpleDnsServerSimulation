import socket

from dns.dns_message import DnsMessage
from dns.recursive_resolver.dns_message_cache import DnsMessageCache
from request_server import RequestServer
from logger import logger


class RecursiveResolver:
    """
    A recursive resolver,
    which accepts recursive dns requests and processes it.
    Uses a DnsMessageCache to cache the last messages
    and clear them after their ttl.
    Can be started by the method run() and stopped by the stop().
    Uses a RequestServer to accept the requests and send the responses.
    """

    def __init__(self,
                 root_dns_server: str, root_dns_server_port: int = 53053,
                 ip_address: str = "127.0.0.10", port: int = 53053):
        self.root_dns_server = root_dns_server
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.root_dns_server_addr = (root_dns_server, root_dns_server_port)
        self.server = RequestServer(
            ip_address, port,
            self.handle_request
        )
        self.cache = DnsMessageCache(logger_key=self.server)

    def run(self) -> None:
        """
        Opens the socket and starts receiving requests in a new thread.
        """
        logger.log("RecursiveResolver:")
        self.server.open_socket()
        self.server.run()  # will be in background
        logger.flush()

    def stop(self) -> None:
        """
        Stop listening for requests,
        the socket will remain blocked.
        """
        self.server.stop_listening()

    def handle_request(self, request: str) -> str:
        """
        Handles a DNS request, which can ba recursive.
        After resolving the possibly recursive request,
        a JSON response is generated and returned as string.
        :param request: The received request.
        :return: The response.
        """
        logger.log(f"RecResolver handling: {request}", self.server)
        dns_request = DnsMessage.new_dns_request(request)
        requested_name = dns_request.get_requested_name()
        dns_resp = self.cache.get_dns_message(requested_name)
        if dns_resp is None:
            logger.log("RecResolver starting resolving...", self.server)
            dns_resp = self._send_root_req(request)
            if dns_request.is_recursion_desired():
                dns_resp = self._resolve_recursion(
                    request, requested_name, dns_resp
                )
            self.cache.add_dns_message(requested_name, dns_resp)
        else:
            logger.log("Cache hit!", self.server)
        dns_resp.set_authoritative(False)
        logger.flush(self.server)
        return dns_resp.build_message()

    def _resolve_recursion(self,
                           original_request: str, requested_name: str,
                           last_dns_resp: DnsMessage) -> DnsMessage:
        name_server_name = last_dns_resp.get_name_server_name()
        while name_server_name is not None \
                and name_server_name != requested_name:
            name_server_addr = last_dns_resp.get_address()
            last_dns_resp = self._send_req(original_request, name_server_addr)
            name_server_name = last_dns_resp.get_name_server_name()
        return last_dns_resp

    def _send_root_req(self, request: str) -> DnsMessage:
        dns_resp = self._send_req(request, *self.root_dns_server_addr)
        return dns_resp

    def _send_req(self, request, server_addr: str, server_port: int = 53053):
        self.udp_sock.sendto(request.encode(), (server_addr, server_port))
        resp_data, _ = self.udp_sock.recvfrom(4096)
        dns_resp = DnsMessage.new_dns_response(resp_data.decode())
        return dns_resp
