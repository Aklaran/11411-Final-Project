# this is a test of the spacy tokenization function

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple isn't looking at buying U.K. startup for $1 billion. I am looking at buying Google for $1.")

preprocessed_doc = []

for sent in doc.sents:

    print(sent.text)
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
            'ent_type': ent_type
            }
            
        sentence.append(token_dict)
        print('text: ', token_dict['lemma'], 'iob: ', token_dict['ent_iob'], 'type: ', token_dict['ent_type'])
    
    preprocessed_doc.append(sentence)



