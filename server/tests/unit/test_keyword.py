from keybert import KeyBERT


def test_pull_key_words():

    text = """A neutron star is the collapsed core of a massive supergiant
            "star, which had a total mass of between 10 and 25 solar masses,
            "possibly more if the star was especially metal-rich.[1] Neutron
            "stars are the smallest and densest stellar objects, excluding
            "black holes and hypothetical white holes, quark stars, and strange
            "stars.[2] Neutron stars have a radius on the order of 10
            "kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They
            "result from the supernova explosion of a massive star, combined
            "with gravitational collapse, that compresses the core past white
            "dwarf star density to that of atomic nuclei."""

    kw_model = KeyBERT()
    # keywords = kw_model.extract_keywords(text)
    keyword_list = (kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 1), stop_words=None))

    assert len(keyword_list) < len(text)
