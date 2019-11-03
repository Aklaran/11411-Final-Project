# this is the main run file for question generation

from copy import deepcopy
import spacy_tokenization as st

class QuestionGenerator:

    def __init__(self, preprocessor):
        tagged_text = preprocessor.processed_doc

        wh_questions = self.generateWhQuestions(tagged_text)
        binary_questions = self.generateBinaryQuestions(tagged_text)

        print(wh_questions)
        print(binary_questions)

    def generateWhQuestions(self, taggedText):
        output = []
        for sentence in taggedText:
            sentenceCopy = deepcopy(sentence)
            question = False

            for word in sentenceCopy:
                if word['ent_type'] == 'PER':
                    question = True
                    word['text'] = 'who'
                if word ['ent_type'] == 'LOC':
                    question = True
                    word['tect'] = 'where'
                if word ['ent_type'] == 'ORG':
                    question = True
                    word['text'] = 'what'
            
            if question:
                out = " ".join([x['text'] for x in sentenceCopy])
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


