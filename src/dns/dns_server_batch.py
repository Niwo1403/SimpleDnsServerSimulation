# local libraries
from dns.simple_dns_server import SimpleDnsServer


class DnsServerBatch:
    """
    A batch of DNS servers,
    witch can be used to create, run and stop multiple DNS servers.
    """

    GENERIC_ZONE_LOC = "../rsrc/zone_files/{}.zone"

    @classmethod
    def get_full_filename(cls, name: str) -> str:
        return cls.GENERIC_ZONE_LOC.format(name)

    def __init__(self, ip_zone_map: {str: str}, port: int = 53053):
        self.dns_servers = [
            SimpleDnsServer(
                DnsServerBatch.get_full_filename(zone_file),
                ip_address, port
            )
            for ip_address, zone_file in ip_zone_map.items()
        ]
        assert len(self.dns_servers) >= 0, \
            "Error, there should at least be one server."

    def run_all(self, log_separator: bool = True) -> None:
        for dns_server in self.dns_servers:
            dns_server.run()
            if log_separator:
                print("---------------")

    def stop_all(self) -> None:
        for dns_server in self.dns_servers:
            dns_server.stop_listening()
