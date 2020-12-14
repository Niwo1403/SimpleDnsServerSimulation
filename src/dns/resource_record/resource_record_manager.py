# local libraries
from dns.resource_record.resource_record import ResourceRecord
from dns.dns_message import DnsMessage
from logger import logger


class ResourceRecordManager:
    """
    Manages all ResourceRecords from a zone file or list.
    Offers the get_match() method,
    which can be used to get the resource record, with the passed name.
    """

    @classmethod
    def from_file(cls, filename: str) -> 'ResourceRecordManager':
        """
        Loads all resource dns_messages from a zone file
        and returns a ResourceRecordManager containing them.
        """
        resource_records = cls.load_resource_records(filename)
        return ResourceRecordManager(resource_records)

    @classmethod
    def load_resource_records(cls, filename: str) -> [ResourceRecord]:
        with open(filename) as zone_file:
            resource_record_entries = zone_file.read().split("\n")
        resource_records = [
            ResourceRecord.from_csv(entry) for entry in resource_record_entries
        ]
        return resource_records

    @staticmethod
    def _get_requested_name(request: DnsMessage or str) -> str:
        return request.get_requested_name() \
            if type(request) != str else request

    def __init__(self, resource_records: [ResourceRecord]):
        self.resource_records = {}
        for resource_record in resource_records:
            self.resource_records[resource_record.get_name()] = resource_record

    def get_matched_record(self,
                           request: DnsMessage or str
                           ) -> ResourceRecord or None:
        """
        Returns the first resource record, which matches the name.
        If no match is found, None is returned.
        """
        requested_name = self._get_requested_name(request)

        closest_match_key = ""
        closest_match_value = None
        for key in self.resource_records:
            if len(closest_match_key) < len(key) \
                    and requested_name.endswith(key):
                closest_match_key = key
                closest_match_value = self.resource_records[key]
        return closest_match_value

    def log_entries(self, logger_key: object = None) -> None:
        for record in self.resource_records.values():
            logger.log(" ".join([
                record.name, str(record.ttl),
                record.rr_class, record.rr_type, record.value
            ]), logger_key)
