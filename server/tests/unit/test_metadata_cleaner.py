from website.utilities.youtube_scraper_lib.cleaners.metadata_cleaner \
    import MetaDataCleaner

CLEANER = MetaDataCleaner()


def test_full_clean_functions_correctly():

    data = {'likes': '1,234',
            'views': '12,345,213',
            'published_at': '3 years ago'}
    CLEANER.full_clean(data)
    assert data['likes'] == 1234
    assert data['views'] == 12345213
    assert len(data['published_at'].split("-")) == 3


def test_format_number_returns_in_integer_format():

    num = CLEANER.format_number("1,234,2")
    assert num == 12342
    num = CLEANER.format_number("dhasd")
    assert num == 0


def test_format_date_returns_in_correct_format():

    date = "2 months ago"
    formatted = CLEANER.format_date(date)
    assert len(formatted.split("-")) == 3
