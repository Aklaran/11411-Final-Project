# module for finding similar sentence in doc

import spacy

class Find:
    """
    finds the most similar sentence in a document
    inputs: question (string), doc (string), 
    returns: sentence (spacy string object)
    """

    def __init__(self, query, input_text):
        
        nlp = spacy.load('en_core_web_md')
        # stopwords = spacy.lang.en.stop_words.STOP_WORDS

        doc = nlp(input_text)

        candidates = []
        for sent in doc.sents:
            candidate = nlp(str(sent))
            score = nlp(query).similarity(candidate)
            candidates.append((score, candidate))
        
        print(candidates)
        self.most_similar = max(candidates, key=lambda x: x[0])[1]


question = 'What is an extinct genus of great ape?'
input_text = 'Danuvius is an extinct genus of great ape that lived 11.6 million years ago during the Middle–Late Miocene in southern Germany. The area at this time was probably a woodland with a seasonal climate. A male specimen was estimated to have weighed about 31 kg (68 lb), and two females 17 and 19 kg (37 and 42 lb).'
most_similar = Find(question, input_text).most_similar
print(most_similar)


