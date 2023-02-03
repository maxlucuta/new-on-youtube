import pytest
from website.utilities import gpt3

INSTRUCTION = "Please summarise this text for me in a few sentences: "
SUFFIX = "\n\ntl;dr"

def test_gpt_api():

    text = """A neutron star is the collapsed core of a massive supergiant 
            "star, which had a total mass of between 10 and 25 solar masses, 
            "possibly more if the star was especially metal-rich.[1] Neutron 
            "stars are the smallest and densest stellar objects, excluding 
            "black holes and hypothetical white holes, quark stars, and strange  
            "stars.[2] Neutron stars have a radius on the order of 10 kilometres 
            "(6.2 mi) and a mass of about 1.4 solar masses.[3] They result from 
            "the supernova explosion of a massive star, combined with gravitational 
            "collapse, that compresses the core past white dwarf star density to 
            "that of atomic nuclei."""

    to_process = INSTRUCTION + text + SUFFIX
    summary = gpt3.summarize_yt_script_with_gpt3(to_process)

    assert len(summary) < len(text)





