# std libraries
from sys import argv
from time import sleep
# local libraries
from connection_argument_extractor import ConnectionArgumentExtractor
from dns.resource_record.resource_record import ResourceRecord
from dns_message import DnsMessage
from request_server import RequestServer
from dns.resource_record.resource_record_manager import ResourceRecordManager


class SimpleDnsServer:
    """
    A DNS server, which handles all incoming DNS lookup request.
    The class only support a very simple version of DNS requests.
    It will load it's resource records from a zone file,
    which must be passed initially as well as the ip address.
    The run() method can be used to start the server.
    The handle_request() method will be called for incoming requests
    to process them.
    """

    @staticmethod
    def _match_types(record: ResourceRecord, request_msg: DnsMessage) -> bool:
        found_match = False
        if record is not None:
            record_type = record.get_type()
            found_match = request_msg.match_type(record_type)
        return found_match

    @staticmethod
    def _dns_resp_from_match(match: ResourceRecord or None) -> DnsMessage:
        matched_req = match is not None
        dns_resp = DnsMessage.new_dns_response()
        if matched_req:
            possible_name = match.get_name() if match.get_type() == "NS" else None
            dns_resp.set_resp(match.value, ttl=match.ttl, name_server_name=possible_name)
        else:
            dns_resp.set_empty_resp()
        return dns_resp

    def __init__(self, zone_file: str, ip_address: str, port: int = 53053):
        self.record_manager = ResourceRecordManager.from_file(zone_file)
        self.ip_address = ip_address
        self.port = port
        self._ensure_connection_information()
        self.server = RequestServer(
            self.ip_address, self.port,
            self.handle_request, log_requests=True
        )  # TODO: Deactivate logging later.

    def run(self, in_background: bool = True) -> None:
        """
        Opens the socket and starts receiving requests.
        Will only return after KeyboardInterrupt.
        """
        self.record_manager.log_entries()
        self.server.open_socket()
        self.server.run()  # will be in background
        if not in_background:
            self.run_till_interrupt()

    def handle_request(self, request: str) -> str:
        """
        Called to handle a request.
        Should find the ip address of the domain.
        :param request: The received request as string, containing the domain.
        :return: The response to answer the client.
        """
        match = self._get_match(request)
        dns_resp = self._dns_resp_from_match(match)
        return dns_resp.build_message()

    def _get_match(self, request: str) -> ResourceRecord:
        request_msg = DnsMessage.new_dns_request(request)
        record = self.record_manager.get_match(request_msg)
        match_found = self._match_types(record, request_msg)
        match = record if match_found else None
        return match

    def stop_listening(self) -> None:
        """
        Stops listening for requests.
        The socket won't be removed.
        """
        self.server.stop_listening()

    def run_till_interrupt(self) -> None:
        while True:
            try:
                sleep(60)
            except KeyboardInterrupt:  # Ctrl + C
                print("Processing stopped, socket will remain blocked.")
                break
        self.stop_listening()

    def _ensure_connection_information(self) -> None:
        if type(self.port) == str and self.port.isnumeric():
            self.port = int(self.port)
        assert type(self.ip_address) == str and len(self.ip_address) >= 7, \
            "Ip address missing."
        assert type(self.port) == int, "Port must be numeric."


def started_as_main() -> bool:
    return __name__ == "__main__"


if started_as_main():
    arg_ip, arg_port = ConnectionArgumentExtractor(argv).get_arguments()
    dns_server = SimpleDnsServer(
        "../rsrc/zone_files/root.zone",
        arg_ip, arg_port
    )
    dns_server.run(in_background=False)
