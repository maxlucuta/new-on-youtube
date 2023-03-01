from .data_cleaner import DataCleaner
import dateparser


class MetaDataCleaner(DataCleaner):
    """Main class for raw metadata cleaning."""

    def __init__(self):
        """Constructs a MetaDataCleaner object."""

        self.data = None

    def full_clean(self, data: list[dict]):
        """Applies all formatting methods to original raw data parsed
           into constructor.

        Raises:
            ValueError: if data not parsed into constructor
        """

        self.data = data
        for key in self.data:
            key['views'] = self.format_number(key['views'])
            key['likes'] = self.format_number(key['likes'])
            key['published_at'] = self.format_date(key['published_at'])

    def format_number(self, number: str) -> int:
        """Transforms a raw number into an int.

        Args:
            number (str): raw representation of number

        Returns:
            int: processed representation of number
        """

        cleaned = "".join([i for i in number if i.isdigit()])
        return int(cleaned) if cleaned else 0

    def format_date(self, date: str) -> str:
        """Transforms a string representation if a date in the form:
           'x year/month/day ago' into 'yy-mm-dd'.

        Args:
            date (str): raw date

        Returns:
            str: formatted date
        """

        formatted_date = dateparser.parse(date)
        return formatted_date.strftime("%Y-%m-%d")
