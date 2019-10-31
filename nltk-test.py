# this is a test of the nltk library

import nltk

sentence = """The first Pharaoh of the Old Kingdom was Djoser (sometime between 2691 and 2625 BC) of the third dynasty, who ordered the construction of a pyramid (the Step Pyramid) in Memphis' necropolis, Saqqara. An important person during the reign of Djoser was his vizier, Imhotep."""
tokens = nltk.word_tokenize(sentence)
#[print(t) for t in tokens]

tagged = nltk.pos_tag(tokens)
[print(t) for t in tagged]

entities = nltk.chunk.ne_chunk(tagged)
#print(entities)