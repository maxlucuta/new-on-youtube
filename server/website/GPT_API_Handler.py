"""
Patricks stuff goes here..
Feel free to change file name or add more, or create a seperate directory to store your stuff, 
if you do, make sure it is within /backend.
"""




# text-davinci-003
# Most capable GPT-3 model. Can do any task the other models can do, often with higher quality, longer output and better instruction-following. Also supports inserting completions within text.
# MAX REQUEST: 4,000 tokens

import os
import openai

openai.api_key = "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"
#openai.api_key = os.getenv("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")

# This used the TL;DR method see end of prompt
response = openai.Completion.create(
    model="text-davinci-003",
    prompt="A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr",
    temperature=0.7,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
)

print(response)
# Temperature: One of the most important settings to control the output of the GPT-3 engine is
# the temperature. This setting controls the randomness of the generated text. A value of 0 makes
# the engine deterministic, which means that it will always generate the same output for a given
# input text.

# top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the
# results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top
# 10% probability mass are considered

# Presence penalty does not consider how frequently a word has been used, but just if the word exists in
# the text. The difference between these two options is subtle, but you can think of Frequency Penalty
# as a way to prevent word repetitions, and Presence Penalty as a way to prevent topic repetitions.

############################################################################################################
############################################################################################################


#openai.api_key = "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"
#openai.api_key = os.getenv("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")

# This used the TL;DR method see end of prompt
response = openai.Completion.create(
    model="text-curie-001",
    prompt="A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr",
    temperature=0.7,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
)

print(response)
# Temperature: One of the most important settings to control the output of the GPT-3 engine is
# the temperature. This setting controls the randomness of the generated text. A value of 0 makes
# the engine deterministic, which means that it will always generate the same output for a given
# input text.

# top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the
# results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top
# 10% probability mass are considered

# Presence penalty does not consider how frequently a word has been used, but just if the word exists in
# the text. The difference between these two options is subtle, but you can think of Frequency Penalty
# as a way to prevent word repetitions, and Presence Penalty as a way to prevent topic repetitions.

############################################################################################################
############################################################################################################