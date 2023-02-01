from keybert import KeyBERT


def pull_key_words(transcript_or_summary):
    """ Uses keybert lib to deduce and fetch keywords for video 
        summaries/transcripts, returning processed data to be 
        stored in ???? database.
        Args:
            transcript_or_summary: string -> video transcript or 
            video summary  
        Returns:
            transcript: [(word, ngram)] in the format found in models.py
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(transcript_or_summary)
    keyword_list = (kw_model.extract_keywords(
        transcript_or_summary, keyphrase_ngram_range=(1, 1), stop_words=None))
    return keyword_list
