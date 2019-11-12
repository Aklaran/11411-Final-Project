#!/usr/bin/env python3

from copy import deepcopy
import preprocess as st
import spacy

import sys

class QuestionGenerator:

    def generateWhQuestions(self, doc):
        output = []

        for sentence in doc.sents:
            is_question = False
            question = []
            main_verb = None
            main_verb_found = False

            for token in sentence:
                # looking for the nominal subject of the sentence...
                if token.dep_ == 'nsubj' and token.head.pos_ == 'VERB':

                    # construct a wh- question where the answer is the nominal object
                    chunk = next((chunk for chunk in doc.noun_chunks if chunk.root == token), None)
                    if chunk:
                        # exclude pronominal phrases and 'who'
                        if chunk.root.tag_ not in ["PRP", "WP"]: 
                            output.append(self.generateWhObjQuestion(chunk))

                    # try to get a wh- pronoun for the subject
                    # FIXME: this only gets possible pronouns for named entities. Should be expended.
                    possible_pronoun = self.replaceWhSubject(token)

                    # if a pronoun exists, replace the word, mark this as a valid question and begin constructing the question
                    if possible_pronoun:
                        is_question = True
                        main_verb = token.head
                        question.append(possible_pronoun) # TODO:later, will want to append whole token for synonyms. for now, just string.
                
                # if a nominal subject has been found, start constructing the rest of the sentence
                if is_question:
                    # waiting till we see the main verb because we don't want to append any extra words from the nsubj's noun chunk
                    if main_verb and token == main_verb:
                        main_verb_found = True
                    
                    # once we've found the main verb, begin appending tokens 
                    if main_verb_found:
                        question.append(token.text)
            
            # construct the question string and add to output
            if len(question) > 0:
                out = " ".join([x for x in question[:-1]]) # indexing till -1 to avoid final punctuation
                out += "?"
                out = out.capitalize()

                output.append(out)
        
        return output
    
    def generateWhObjQuestion(self, chunk):
        # FIXME: Get the right wh- word for the questions!

        # change 'to be' inflection for plural words
        # spacy.Token.tag denotes plural words with a final 'S'
        if chunk.root.tag_.endswith('S'):
            linking_verb = 'are'
        else:
            linking_verb = 'is'

        # only capitalize proper names
        # using non-null entity types as a proxy
        if chunk.root.ent_type_ == '':
            text = chunk.text.lower()
        else:
            text = chunk.text

        return "What " + linking_verb + " " + text + "?"

    def replaceWhSubject(self, subj):
        # dictionary to map from entity types to wh- pronouns
        switcher = {
            'PERSON': 'who',
            'LOC': 'where',
            'ORG': 'what'
        }
        
        return switcher.get(subj.ent_type_, None)

if __name__ == "__main__":
    # Ensure 2 arguments
    if len(sys.argv) != 3:
        print("Usage: ./ask ARTICLE_TXT NUM_QUESTIONS")
        sys.exit(1)

    # Read string from 1 text file. 
    # TODO: extend this to a directory of files
    INPUT_TXT = sys.argv[1]
    N_QUESTIONS = sys.argv[2]

    with open(INPUT_TXT, 'r') as file:
        text = file.read()

    # Instantiate our preprocessor and get the processed doc
    preprocesser = st.Preprocessor(text)
    processed_doc = preprocesser.doc

    # Instantiate our question generator and make some questions
    question_generator = QuestionGenerator()

    wh_questions = question_generator.generateWhQuestions(processed_doc)
    for question in wh_questions:
        print(question)
