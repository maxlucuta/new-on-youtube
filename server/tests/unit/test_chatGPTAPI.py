"""
This file contains the function that sends a transcript from a 
YT video to the gpt3 API and returns a summary of the transcript. 

Key Facts: 
    - The language model used in openai's backend is davinci-003.
    - The maximum request is 4000 tokens. 

"""

#necessary library 
import openai

def summarize_yt_script_with_gpt3(yt_transcript, temperature, max_tokens, 
                                  top_p, frequency_penalty, presence_penalty):
    """
    This function sends a transcript from a YT video to 
    the gpt3 API and returns a summary of the transcript.

    Args: 
        yt_transcript (string): The transcript from the YT video. 
        
        temperature (float): A decimal value between 0 and 1. This is 
                    controls the randomness of the generated text. A value of 0 makes
                    the engine deterministic, which means that it will always generate 
                    the same output for a given input text.
        
        max_tokens (int): The maximum number of tokens used. 

        top_p (float): An alternative to sampling with temperature, called nucleus sampling, 
                        where the model considers the results of the tokens with top_p probability mass. 
                        So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        
        presence_penalty (float): Presence penalty does not consider how frequently a word has been used, 
                                  but just if the word exists in the text. The difference between 
                                  these two options is subtle, but you can think of Frequency Penalty
                                  as a way to prevent word repetitions, and Presence Penalty as a way to 
                                  prevent topic repetitions.

    Returns: 
        string: The summary of the transcript of the a given YT video.  

   """                
    openai.api_key = "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"
    response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = yt_transcript,
                    temperature = temperature,
                    max_tokens = max_tokens,
                    top_p = top_p,
                    frequency_penalty = frequency_penalty,
                    presence_penalty = presence_penalty)

    return response['choices'][0]['text'] 

if __name__ == "__main__":
    yt_transcript = "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr"
    summary = summarize_yt_script_with_gpt3(yt_transcript, 0.7, 60, 1.0, 0, 1)
    print(summary)
