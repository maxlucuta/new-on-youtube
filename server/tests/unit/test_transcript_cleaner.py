from website.utilities.youtube_scraper_lib.cleaners.transcript_cleaner \
    import TranscriptCleaner

CLEANER = TranscriptCleaner()
DATA = [{'text': "Hello"}, {'text': "[Music]"}]


def test_format_clean_removes_music_text():

    cleaned = CLEANER.format_strings(DATA)
    assert cleaned == "Hello"


def test_full_clean():

    data = [{'transcript': DATA}, {'transcript': DATA}]
    CLEANER.full_clean(data)
    for key in data:
        assert key['transcript'] == "Hello"
