# this is a text preprocessor module built using spacy and neuralcoref

import spacy
import pprint
import neuralcoref

# pretty printing for debugging purposes
pp = pprint.PrettyPrinter()

class Preprocessor:
    def __init__(self, input_text):

        # load spacy processor and add neuralcoref function
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)

        # define text (change to pipeline for final version)
        self.doc = nlp(input_text)

        # process text
        self.processed_doc = self.process(self.doc)
        self.coref = self.doc._.coref_clusters

        # print processed texts (for testing only, delete for final version)
        # print(self.processed_doc)
        # print(self.coref)

    # process()
    # inputs: doc (string)
    # returns: doc list containing sentence list of token dictionaries (2D list of dictionaries)
    def process(self, doc):

        preprocessed_doc = []
        for sent in doc.sents:

            # print(sent.text)
            sentence = []
            for token in sent:

                # check for token corefs
                if token._.in_coref:
                    coref = token._.coref_clusters
                else:
                    coref = None
                
                # determine entity type and iob
                ent_iob = token.ent_iob_
                ent_type = token.ent_type_

                # build dictionary
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
                    'coref': coref
                    }
                    
                sentence.append(token_dict)

                # sample coref resolution (print main coref)
                # if coref:
                #     #print(token_dict['text'], ':', coref[0].main)
                # else:
                #     print(token_dict['text'], ': None')
            
            preprocessed_doc.append(sentence)
        
        return preprocessed_doc

# local testing (delete for final version)
# prep = Preprocessor()