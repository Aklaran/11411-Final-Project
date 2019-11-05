# this is a test of the spacy tokenization function

import spacy
import pprint
import neuralcoref

pp = pprint.PrettyPrinter()

class Preprocessor:
    def __init__(self):
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        doc = nlp("Apple isn't looking at buying U.K. startup for $1 billion.")

        self.processed_doc = self.process(doc)
        self.coref = doc._.coref_clusters

    #   print(self.processed_doc)
        # print(self.coref)

    def process(self, doc):
        preprocessed_doc = []
        
        for sent in doc.sents:

            # print(sent.text)
            sentence = []

            for token in sent:

                ent_iob = token.ent_iob_
                ent_type = token.ent_type_
                token_dict = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'tag': token.tag_, 
                    'dep': token.dep_,
                    'shape': token.shape_, 
                    'alpha': token.is_alpha, 
                    'stop': token.is_stop,
                    'ent_iob': ent_iob,
                    'ent_type': ent_type,
                    'headPos': token.head.pos_
                    }
                    
                sentence.append(token_dict)
            
            preprocessed_doc.append(sentence)
        
        # print(preprocessed_doc)
        return preprocessed_doc