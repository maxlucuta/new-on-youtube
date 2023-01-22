
#import os, sys
#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
#sys.path.append(parentdir)

from website.utilities.gpt3 import summarize_yt_script_with_gpt3
from website.utilities.database import establish_connection, query_yt_videos





yt_transcript = "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr"

response = summarize_yt_script_with_gpt3(yt_transcript)

print(response)

print ("  ------------------------- TESTING DB QUERY -----------------------------------------")

conn = establish_connection()
res = query_yt_videos('football', 2, conn)
print(res)

