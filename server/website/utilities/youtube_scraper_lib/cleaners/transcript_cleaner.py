from .data_cleaner import DataCleaner


class TranscriptCleaner(DataCleaner):
    """Main class for cleaning raw transcripts scraped from YouTube."""

    def __init__(self):
        """Constructs a TranscriptCleaner object."""

        self.data = None

    def full_clean(self, data: list[dict]):
        """Applies all formatting methods to original raw data parsed
           into constructor.

        Args:
            data (list[dict], optional): list of dict containing raw
            transcripts obatined from YouTube transcript scraping
        """
        self.data = data
        for key in self.data:
            key['transcript'] = self.format_strings(key['transcript'])

    def format_strings(self, transcript: str) -> str:
        """Formats raw transcript.

        Args:
            transcript (str): raw transcript
        Returns:
            str: processed transcript
        """

        final_transcript = []
        for text in transcript:
            word = text.get('text')
            if not word or word == '[Music]':
                continue
            final_transcript.append(word)
        return " ".join(final_transcript)
