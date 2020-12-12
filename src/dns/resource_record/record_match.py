# local imports
from dns.resource_record.resource_record import ResourceRecord


class RecordMatch:
    """
    A match of a ResourceRecord, which matches a DNS request.
    Can be empty if no match found.
    Offers methods to access the values of the record,
    but these should only be used if a record was found.
    If the RecordMatch found a record,
    can be tested by calling the found_record() method.
    """

    def __init__(self, resource_record: ResourceRecord):
        self.resource_record = resource_record

    def found_record(self) -> bool:
        return self.resource_record is not None

    def get_possible_name_server_name(self) -> str or None:
        return self.resource_record.get_name() if self._is_name_server_record() else None

    def get_value(self) -> str:
        return self.resource_record.value

    def get_ttl(self) -> int:
        return self.resource_record.ttl

    def _is_name_server_record(self) -> bool:
        return self.resource_record is not None and self.resource_record.get_type() == "NS"
