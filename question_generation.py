# this is the main run file for question generation

from copy import deepcopy
import preprocess as st
import spacy

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
                    if chunk :output.append(self.generateWhObjQuestion(chunk))

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
        return "What is " + chunk.text + "?"

    def replaceWhSubject(self, subj):
        # dictionary to map from entity types to wh- pronouns
        switcher = {
            'PERSON': 'who',
            'LOC': 'where',
            'ORG': 'what'
        }
        
        return switcher.get(subj.ent_type_, None)
