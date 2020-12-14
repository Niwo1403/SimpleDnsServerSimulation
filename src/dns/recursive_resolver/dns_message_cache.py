# std. imports
from datetime import datetime, timedelta
# local imports
from dns.dns_message import DnsMessage
from logger import logger


class DnsMessageCache:
    """
    A cache for DnsMessages, which contains the last responses,
    if their ttl is not expired.
    Contains for each requested name the ttl and the old response message.
    A new response can be generated from the old response,
    by adjusting the object as required.
    DnsMessages can be accessed using the add_dns_message()
    and get_dns_message() method.
    The ttl can be updated by calling update_dns_messages(),
    which will be done automatically by calling get_dns_message().
    """

    @staticmethod
    def _get_record_expiry_timestamp(dns_msg: DnsMessage) -> datetime:
        return datetime.now() + timedelta(0, dns_msg.get_ttl())

    def __init__(self, logger_key: object = None):
        self.dns_messages: {str: (datetime, DnsMessage)} = {}
        self.logger_key = logger_key

    def add_dns_message(self,
                        requested_name: str,
                        dns_response: DnsMessage) -> None:
        """
        Adds a response by it's name, as well as the DnsMessage,
        witch was received as response from a name server.
        :param requested_name: The name of the request - e.g. pcpools.fuberlin
        :param dns_response: An object of DnsMessage,
        containing the received response.
        """
        self.dns_messages[requested_name] = (
            self._get_record_expiry_timestamp(dns_response),
            dns_response
        )

    def get_dns_message(self, req_name: str) -> DnsMessage:
        """
        Searches for a request in the cache by its name.
        Before looking up the request,
        the cache will be updated (see update_dns_msg()).
        :param req_name: The name to lookup in the cache.
        :return: The DnsMessage containing the cached response.
        """
        logger.log(f"Cache got request for {req_name}", self.logger_key)
        self.update_dns_messages()
        dns_msg = self._get_best_record_match(req_name)
        return dns_msg

    def update_dns_messages(self) -> None:
        """
        Updates the DnsMessages, by removing all messages,
        which got an expired timestamp.
        The timestamp is initially generated from the ttl and system time.
        """
        now = datetime.now()
        self.dns_messages = {
            requested_name: time_msg_tuple
            for requested_name, time_msg_tuple in self.dns_messages.items()
            if time_msg_tuple[0] > now
        }

    def _get_best_record_match(self, req_name: str) -> DnsMessage:
        best_match_name = ""
        best_match_msg = None
        for record_name in self.dns_messages:
            if len(record_name) > len(best_match_name) \
                    and req_name.endswith(record_name):
                best_match_name = record_name
                best_match_msg = self.dns_messages[record_name][1]  # 0 = timestamp, 1 = DNS message
        if best_match_msg is not None:
            self._update_msg_ttl(best_match_name)
        return best_match_msg

    def _update_msg_ttl(self, best_match_name: str) -> None:
        expiry_timestamp, dns_msg = self.dns_messages[best_match_name]
        updated_ttl = expiry_timestamp - datetime.now()
        dns_msg.set_updated_ttl(updated_ttl.seconds)
