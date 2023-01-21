
"""
import os
import openai


def summarize_yt_script_with_gpt3(yt_transcript):
    openai.api_key = "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"
    
    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt= yt_transcript,
                    temperature=0.7,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=1
                )

    return response 



test_transcript = "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr"
summary = summarize_yt_script_with_gpt3(test_transcript)
print(summary)
"""