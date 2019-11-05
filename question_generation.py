# this is the main run file for question generation

from copy import deepcopy
import spacy_tokenization as st

class QuestionGenerator:

    def __init__(self, preprocessor):
        tagged_text = preprocessor.processed_doc

        wh_questions = self.generateWhQuestions(tagged_text)

        print(wh_questions)

    def generateWhQuestions(self, taggedText):
        output = []

        for sentence in taggedText:
            question = False

            for possible_subject in sentence:
                if possible_subject['dep'] == 'nsubj' and possible_subject['headPos'] == 'VERB':
                    # print(possible_subject['text'] + ' ' + possible_subject['ent_type'])

                    # replace the subject noun chunk with the appropriate wh- pronoun
                    possible_subject['text'] = self.replaceWhSubject(possible_subject)
                    question = True
                
            # reconstruct the question with a question mark and add it to the output
            if question:
                out = " ".join([x['text'] for x in sentence[:-1]])
                out += "?"

                output.append(out)
        
        return output

    def replaceWhSubject(self, subj):
        # create a dictionary to map from entity types to wh- pronouns
        switcher = {
            'PERSON': 'who',
            'LOC': 'where',
            'ORG': 'what'
        }
        
        return switcher.get(subj['ent_type'], None)           

def main():
    qg = QuestionGenerator(st.Preprocessor())

if __name__ == "__main__":    
    main()
