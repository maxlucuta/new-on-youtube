class DataCleaner:
    """Abstract class for DataCleaner."""

    def __init__(self, *args, **kwargs):
        """Abstract implementation of constructor."""

        raise NotImplementedError()

    def format_number(self, *args, **kwargs):
        """Abstract implementation of number formatting method."""

        raise NotImplementedError()

    def format_string(self, *args, **kwargs):
        """Abstract implementation of string formatting method."""

        raise NotImplementedError()

    def format_date(self, *args, **kwargs):
        """Abstract implementation of date formatting method."""

        raise NotImplementedError()

    def full_clean(self, *args, **kwargs):
        """Abstract implementation of data cleaning method."""

        raise NotImplementedError()

    @staticmethod
    def occupied_fields(data: dict, expected: int):
        """Checks if the given data has the expected number of fields,
           and if the fields all consist of non-null values.

        Args:
            data (dict): data to check
            expected (int): expected number of fields in data

        Returns:
            bool: true if all above passes, false otherwise
        """

        for key in data:
            if not data[key]:
                return False
        return len(data) == expected
