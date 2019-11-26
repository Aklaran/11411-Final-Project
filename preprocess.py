# this is a text preprocessor module built using spacy and neuralcoref

import spacy
import neuralcoref
import benepar

from benepar.spacy_plugin import BeneparComponent

class Preprocessor:
    def __init__(self, input_text):

        # load spacy processor and add neuralcoref function
        nlp = spacy.load("en_core_web_sm")

        neuralcoref.add_to_pipe(nlp, greedyness=0.53125)

        benepar.download('benepar_en2', quiet=True)
        nlp.add_pipe(BeneparComponent("benepar_en2"))

        # define text (change to pipeline for final version)
        self.doc = nlp(input_text)

        # process text
        self.processed_doc = self.process(self.doc)
        #self.coref = self.doc._.coref_clusters

    # process()
    # inputs: doc (string)
    # returns: doc list containing sentence list of token dictionaries (2D list of dictionaries)
    def process(self, doc):

        preprocessed_doc = []

        #Noun chunks are “base noun phrases” – flat phrases that have a noun as their 
        #head. You can think of noun chunks as a noun plus the words describing the 
        #noun – for example, “the lavish green grass” or “the world’s largest tech fund”
        
        #https://spacy.io/usage/linguistic-features#dependency-parse

        #can also get list of chunks: chunks = list(doc.noun_chunks)
        chunk_list = []
        for chunk in doc.noun_chunks:
            chunkdict = {
                'chunk_test': chunk.text,
                'chunk_root_text': chunk.root.text,
                #string value .dep_, hash value .dep
                'chunk_root_dep': chunk.root.dep_,
                'chunk_root_head': chunk.root.head.text
                }
            chunk_list.append(chunkdict)

        for sent in doc.sents:

            # print(sent.text)
            sentence = []
            for token in sent:

                # # check for token corefs
                # if token._.in_coref:
                #     coref = token._.coref_clusters
                # else:
                #     coref = None
                
                # determine entity type and iob
                ent_iob = token.ent_iob_
                ent_type = token.ent_type_
                ##should this be done with ent.label_

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
                    #'coref': coref,

                    ##for dependency parse: need to consider merging chunk dict as well
                    'head_text': token.head.text,
                    'head_pos': token.head.pos_
                    }
                    
                sentence.append(token_dict)
                #get whole phrase by syntactic head with token.subtree

                # sample coref resolution (print main coref)
                # if coref:
                #     #print(token_dict['text'], ':', coref[0].main)
                # else:
                #     print(token_dict['text'], ': None')
            
            preprocessed_doc.append(sentence)
        
        return preprocessed_doc

        #at end check for doc.is_parsed

# local testing (delete for final version)
# prep = Preprocessor()