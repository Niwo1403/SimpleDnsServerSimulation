def _get_first_numeric(args) -> "First numeric element of the list or None if there is none.":
    numeric_elements = list(filter(str.isnumeric, args))
    numeric_element = numeric_elements[0] if len(numeric_elements) >= 1 else None
    return numeric_element


class ResourceRecord:
    """
    A representation of a resource record.
    Contains the name, value, ttl, rr_class and rr_type of the record.
    """

    @classmethod
    def from_csv(cls, csv_line, delimiter=" ", separate_by_tabs=True):
        """
        Generates a ResourceRecord object from a line of a csv file.
        The line must at least contain the name and value of the record.
        The ttl must be numeric, if included.
        :return: A ResourceRecord object, containing the data from the csv line.
        """
        if separate_by_tabs:
            csv_line = csv_line.replace("\t", delimiter)
        tmp_values = csv_line.split("\"")
        for i in range(len(tmp_values)):
            if i % 2 == 0:
                tmp_values[i] = tmp_values[i].split(delimiter)
            else:
                tmp_values[i] = [tmp_values[i]]
        values = sum(tmp_values, [])
        return cls.load_data_from_list(values)

    @classmethod
    def load_data_from_list(cls, values):
        """
        Generates a ResourceRecord object from list of strings.
        The list must at least contain the name and value of the record.
        The ttl must be a numeric string, if included.
        :return: A ResourceRecord object, containing the data from the csv line.
        """
        filled_values = list(filter(lambda x: x != "", values))
        assert len(filled_values) >= 2, "The values must at least include the name and value."
        name = filled_values[0]
        value = filled_values[-1]
        record = ResourceRecord(name, value)
        record._update_data_from_csv(filled_values[1:-1])
        return record

    def __init__(self, name, value, rr_class="IN", rr_type="NS", ttl=300):
        self.rr_type = rr_type
        self.rr_class = rr_class
        self.ttl = ttl
        self.name = name
        self.value = value

    def matches(self, other_name) -> bool:
        """
        Returns true, if the other_name is equal to the name of the resource record.
        """
        return self.name == other_name

    def get_name(self):
        return self.name

    def _update_data_from_csv(self, values):
        ttl = _get_first_numeric(values)
        if ttl is not None:
            values.remove(ttl)
            self.ttl = ttl
        self._update_string_flags(values)

    def _update_string_flags(self, values):
        value_len = len(values)
        if value_len >= 1:
            self.rr_type = values[-1]
            self.rr_class = values[0] if value_len >= 2 else "IN"
