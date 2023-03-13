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

        data['views'] = self.format_number(data['views'])
        data['likes'] = self.format_number(data['likes'])
        data['published_at'] = self.format_date(data['published_at'])
        self.data = data

    def format_number(self, number: str) -> int:
        """Transforms a raw number into an int.

        Args:
            number (str): raw representation of number

        Returns:
            int: processed representation of number
        """
        try:
            cleaned = "".join([i for i in number if i.isdigit()])
            return int(cleaned) if cleaned else 0
        except (TypeError, ValueError):
            return None

    def format_date(self, date: str) -> str:
        """Transforms a string representation if a date in the form:
           'x year/month/day ago' into 'yy-mm-dd'.

        Args:
            date (str): raw date

        Returns:
            str: formatted date
        """
        if not isinstance(date, str):
            return None
        formatted_date = dateparser.parse(date)
        if not formatted_date:
            return None
        return formatted_date.strftime("%Y-%m-%d")
