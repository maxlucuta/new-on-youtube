"""
This file contains the function that sends a transcript from a
YT video to the gpt3 API and returns a summary of the transcript.

Key Facts:
    - The language model used in openai's backend is davinci-003.
    - The maximum request is 4000 tokens.

"""
import openai
# from keybert import KeyBERT


def summarize_yt_script_with_gpt3(yt_transcript,
                                  temperature=0.7,
                                  max_tokens=100,
                                  top_p=1.0,
                                  frequency_penalty=0.5,
                                  presence_penalty=0.5):
    """
    This function sends a transcript from a YT video to
    the gpt3 API and returns a summary of the transcript.

    Args:
        yt_transcript (string): The transcript from the YT video.

        temperature (float): A decimal value between 0 and 1. This is
                    controls the randomness of the generated text. A
                    value of 0 makes the engine deterministic, which
                    means that it will always generate the same output
                    for a given input text.

        max_tokens (int): The maximum number of tokens used.

        top_p (float): An alternative to sampling with temperature, called
                       nucleus sampling, where the model considers the
                       results of the tokens with top_p probability mass.
                       So 0.1 means only the tokens comprising the top 10%
                       probability mass are considered.

        presence_penalty (float): Presence penalty does not consider how
                                  frequently a word has been used,
                                  but just if the word exists in the text.
                                  The difference between these two options
                                  is subtle, but you can think of Frequency
                                  Penalty as a way to prevent word
                                  repetitions, and Presence Penalty as a way to
                                  prevent topic repetitions.

    Returns:
        string: The summary of the transcript of the a given YT video.

   """
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=yt_transcript,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty)

    return response['choices'][0]['text']


"""
def pull_key_words(summary):
    "" Uses keybert lib to deduce and fetch keywords for video
        summaries/transcripts, returning processed data to be
        stored in the cassandra database.

        Args:
            transcript_or_summary: string -> video transcript or
            video summary

        Returns:
            transcript: [(word, ngram)] in the format found in models.py
    ""
    model = KeyBERT()
    keywords_list = (model.extract_keywords(summary,
                                            keyphrase_ngram_range=(1, 1),
                                            stop_words=None))
    keywords = [i[0] for i in keywords_list]
    return keywords
"""
