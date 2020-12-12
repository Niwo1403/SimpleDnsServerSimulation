import json


class DnsMessage:
    """
    A message, used for DNS requests and responses.
    The build_message() method can be used
    to get a string representation as json string of the message.
    After the constructor the methods as_dns_request() and as_dns_response()
    can be used to set specific default values.
    """

    # https://support.umbrella.com/hc/en-us/articles/232254248-Common-DNS-return-codes-for-any-DNS-service-and-Umbrella-
    R_CODES = {
        "NOERROR": 0,  # DNS Query completed successfully
        "FORMERR": 1,  # DNS Query Format Error
        "SERVFAIL": 2,  # Server failed to complete the DNS request
        "NXDOMAIN": 3,  # Domain name does not exist
        "NOTIMP": 4,  # Function not implemented
        "REFUSED": 5,  # The server refused to answer for the query
        "YXDOMAIN": 6,  # Name that should not exist, does exist
        "XRRSET": 7,  # RR set that should not exist, does exist
        "NOTAUTH": 8,  # Server not authoritative for the zone
        "NOTZONE": 9  # Name not in zone
    }

    QRY_TYPES = {  # only some (the used ones)
        "A": 1,
        "NS": 2
    }

    DEFAULT_SETTINGS = {
        "DNS": {
            "dns.a": None,  # IP Agresse
            "dns.count.answers": None,  # Count of answers
            "dns.flags.authoritative": None,  # True, if authoritative DNS server or False if recursive DNS server
            "dns.flags.rcode": None,  # response code,
            "dns.flags.recdesired": None,  # True, if recursion should be used by the server
            "dns.flags.response": None,  # True, if a result was found
            "dns.ns": None,  # The name of the ns server if there is one
            "dns.qry.name": None,  # name witch is requested
            "dns.qry.type": None,  # requested type - A=1, NS=2
            "dns.resp.ttl": None,  # TTL of the record
            "dns.srv.name": None,  # ?
            "dns.srv.port": None,  # ?
            "dns.srv.proto": None,  # ?
            "dns.srv.service": None,  # ?
            "dns.srv.target": None  # ?
        },
        "DNS_request": {
            "dns.flags.recdesired": False,  # True, if recursion should be used by the server
            "dns.qry.name": "root",  # name witch is requested
            "dns.qry.type": 2,  # requested type - A=1, NS=2
        },
        "DNS_response": {
            "dns.a": "",  # IP Agresse
            "dns.count.answers": 0,  # Count of answers
            "dns.flags.authoritative": True,  # True, if authoritative DNS Server or False if it's a recursive DNS server
            "dns.flags.rcode": R_CODES["NXDOMAIN"],  # response code, more information see above at R_CODES
            "dns.flags.response": False,  # True, if a result was found
            "dns.ns": None,  # The name of the ns server if there is one
            "dns.resp.ttl": 0  # TTL of the record
        }
    }

    @classmethod
    def from_str(cls, encoded_msg: str) -> 'DnsMessage':
        values = json.loads(encoded_msg)
        return DnsMessage(values)

    @classmethod
    def new_dns_request(cls, values: {} or str = None) -> 'DnsMessage':
        """
        Creates a dns request message from the dns message, by setting the dns request default values.
        Should be called directly after the constructor.
        :return: Self, which will be dns request message.
        """
        dns_request = cls._get_basic_object(values)
        dns_req_defaults = cls.DEFAULT_SETTINGS["DNS_request"]
        dns_request.set_values(dns_req_defaults, replace=False)
        return dns_request

    @classmethod
    def new_dns_response(cls, values: {} or str = None) -> 'DnsMessage':
        """
        Creates a dns response message from the dns message, by setting the dns response default values.
        Should be called directly after the constructor.
        :return: Self, which will be dns response message.
        """
        dns_response = cls._get_basic_object(values)
        dns_resp_defaults = DnsMessage.DEFAULT_SETTINGS["DNS_response"]
        dns_response.set_values(dns_resp_defaults, replace=False)
        return dns_response

    @classmethod
    def _get_basic_object(cls, values: {} or str = None) -> 'DnsMessage':
        values = values or {}
        dns_response = DnsMessage.from_str(values)\
            if type(values) == str else cls(values)
        return dns_response

    def __init__(self, values: {}):
        self.values = values
        self._init_basic_request()

    def build_message(self) -> str:
        """
        Creates a JSON string, containing the information of the message.
        """
        return json.dumps(self.values)

    def set_value(self, key: str, value: str or None = None) -> None:
        self.values[key] = value

    def set_values(self, repl_values: {str: str or int or bool or None}, replace: bool = True) -> None:
        """
        Updates the current values by the ones in repl_values.
        If replace is True, existing values will be replaced.
        """
        for key, value in repl_values.items():
            if replace or key not in self.values or self.values[key] is None:
                self.set_value(key, value)

    def get_value(self, key: str) -> str:
        """
        Throws KeyError if key doesn't exist.
        """
        return self.values[key]

    def set_empty_resp(self, authoritative: bool = True):
        self.set_resp("", answers=0, set_positive_rcode=False, authoritative=authoritative)

    def set_resp(self, address: str,
                 answers: int = 1, authoritative: bool = True, set_positive_rcode: bool = True,
                 ttl: int = 0, name_server_name: str or None = None) -> None:
        """
        Sets the data for a response.
        :param address: The ip address.
        :param answers: The count of answers.
        :param authoritative: True,
        if the server is a non recursive DNS server.
        :param set_positive_rcode: Sets the response code to 'NOERROR' (0).
        :param ttl: The TTL of the record.
        :param name_server_name: The name of the name server,
        if there is one, else None.
        """
        value_updates = {
            "dns.a": address,
            "dns.count.answers": answers,
            "dns.flags.authoritative": authoritative,
            "dns.flags.response": True,
            "dns.resp.ttl": ttl,
            "dns.ns": name_server_name
        }
        if set_positive_rcode:
            value_updates["dns.flags.rcode"] = DnsMessage.R_CODES["NOERROR"]
        self.set_values(value_updates)

    def set_req(self,
                name: str, name_server_record: bool = False,
                recursion_desired: bool or None = None) -> None:
        """
        Sets the main data for a request.
        :param name: The domain to lookup.
        :param name_server_record: If name_server_record is False, it will be a A record.
        :param recursion_desired: If recursion_desired is None, it won't be changed.
        """
        value_updates = {
            "dns.qry.name": name,
            "dns.qry.type": 1 + name_server_record
        }
        if recursion_desired is not None:
            value_updates["dns.flags.recdesired"] = recursion_desired
        self.set_values(value_updates)

    def is_recursion_desired(self) -> bool:
        return self.values["dns.flags.recdesired"]

    def get_requested_name(self) -> str:
        return self.values["dns.qry.name"]

    def get_requested_type(self) -> int:
        return self.values["dns.qry.type"]

    def match_type(self, other_type: str) -> bool:
        return DnsMessage.QRY_TYPES[other_type] == self.get_requested_type()

    def is_a_record_request(self) -> bool:
        return self.get_requested_type() == DnsMessage.QRY_TYPES["A"]

    def _is_key_empty(self, key: str) -> bool:
        """
        The key is empty, if the value isn't set or None.
        An empty string won't be recognized as empty.
        """
        return key not in self.values or self.values[key] is None

    def _init_basic_request(self) -> None:
        basic_req_settings = DnsMessage.DEFAULT_SETTINGS["DNS"]
        self.set_values(basic_req_settings, replace=False)


if __name__ == "__main__":
    dns_req = DnsMessage.new_dns_request()
    dns_req.set_req("fuberlin")
    print(dns_req.build_message())

    dns_resp = DnsMessage.new_dns_request()
    dns_resp.set_resp("127.0.0.1")
    print(dns_resp.build_message())
