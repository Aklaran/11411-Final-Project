# this is the main run file for question generation

from copy import deepcopy
import spacy_tokenization as st

class QuestionGenerator:

    def __init__(self, preprocessor):
        tagged_text = preprocessor.processed_doc

        wh_questions = self.generateWhQuestions(tagged_text)
        #binary_questions = self.generateBinaryQuestions(tagged_text)

        print(wh_questions)

    def generateWhQuestions(self, taggedText):
        output = []

        for sentence in taggedText:
            question = False

            for possible_subject in sentence:
                if possible_subject['dep'] == 'nsubj' and possible_subject['headPos'] == 'VERB':
                    print(possible_subject['text'])
                    if possible_subject['ent_type'] == 'PER':
                        question = True
                        possible_subject['text'] = 'who'
                    if possible_subject ['ent_type'] == 'LOC':
                        question = True
                        possible_subject['tect'] = 'where'
                    if possible_subject ['ent_type'] == 'ORG':
                        question = True
                        possible_subject['text'] = 'what'
                
            if question:
                out = " ".join([x['text'] for x in sentence[:-1]])
                out += "?"

                output.append(out)
        
        return output
    
    def generateBinaryQuestions(self, taggedText):
        output = []
        for sentence in taggedText:
            sentenceCopy = deepcopy(sentence)
            question = False

            for i, word in enumerate(sentenceCopy):
                if word['lemma'] == 'be':
                    # FIXME: this is only gonna go back 1 word; it actually needs to go back to the head of the dependency phrase
                    sentenceCopy[i-1], sentenceCopy[i] = word, sentenceCopy[i-1]
                    question = True
            
            if question:
                out = " ".join([x['text'] for x in sentenceCopy])
                out += "?"

                output.append(out)
            
        return output            

def main():
    qg = QuestionGenerator(st.Preprocessor())

if __name__ == "__main__":    
    main()
