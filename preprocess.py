# this is a text preprocessor module built using spacy and neuralcoref

import spacy
import pprint
import neuralcoref

pp = pprint.PrettyPrinter()

class Preprocessor:
    def __init__(self):

        # load spacy processor and add neuralcoref function
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)

        # define text (change to pipeline for final version)
        self.doc = nlp("Guy Fawkes, also known as Guido Fawkes while fighting for the Spanish, was a member of a group of provincial English Catholics who planned the failed Gunpowder Plot of 1605. He was born and educated in York; his father died when Fawkes was eight years old, after which his mother married a recusant Catholic. Fawkes converted to Catholicism and left for mainland Europe, where he fought for Catholic Spain in the Eighty Years' War against Protestant Dutch reformers in the Low Countries. He travelled to Spain to seek support for a Catholic rebellion in England without success. He later met Thomas Wintour, with whom he returned to England. Wintour introduced him to Robert Catesby, who planned to assassinate King James I and restore a Catholic monarch to the throne. The plotters leased an undercroft beneath the House of Lords; Fawkes was placed in charge of the gunpowder which they stockpiled there. The authorities were prompted by an anonymous letter to search Westminster Palace during the early hours of 5 November, and they found Fawkes guarding the explosives. He was questioned and tortured over the next few days and confessed to wanting to blow up the House of Lords.")

        # process text
        self.processed_doc = self.process(doc)
        self.coref = doc._.coref_clusters

        # print processed texts (for testing only, delete for final version)
        # print(self.processed_doc)
        print(self.coref)

    # process()
    # inputs: doc (string)
    # returns: doc list containing sentence list of token dictionaries (2D list of dictionaries)
    def process(self, doc):

        preprocessed_doc = []
        for sent in doc.sents:

            print(sent.text)
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
                if coref:
                    print(token_dict['text'], ':', coref[0].main)
                else:
                    print(token_dict['text'], ': None')
            
            preprocessed_doc.append(sentence)
        
        return preprocessed_doc

# local testing (delete for final version)
prep = Preprocessor()