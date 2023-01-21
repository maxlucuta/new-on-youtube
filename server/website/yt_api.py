from youtube_transcript_api import YouTubeTranscriptApi


def generate_transcripts(key):
    """ Calls youtube_transcript api to return a transcript 
        for a specific video.

        Args:
            key: string -> unique key for video.

        Returns:
            transcript: string -> transcript for the video.
    """
    raw_transcript = YouTubeTranscriptApi.get_transcript(key)
    final_transcript = []

    for text in raw_transcript:
        word = text.get('text')
        if not word or word == '[Music]':
            continue
        final_transcript.append(word)
    
    return " ".join(final_transcript)
        