# this is the main run file for question generation

# import Preprocessor

from copy import deepcopy

tagged_text_spoof = [[{'TOKEN': 'Trump',
                       'POS': 'NNP',
                       'ENT_LABEL': 'PER',
                       'LEMMA': 'Trump'},
                      {'TOKEN': 'is',
                       'POS': 'V',
                       'ENT_LABEL': 'NONE',
                       'LEMMA': 'be'},
                      {'TOKEN': 'mean',
                       'POS': 'ADJ',
                       'ENT_LABEL': 'NONE',
                       'LEMMA': 'mean'},]]

class QuestionGenerator:
    def generateWhoQuestions(self, taggedText):
        output = []
        for sentence in taggedText:
            sentenceCopy = deepcopy(sentence)
            question = False

            for word in sentenceCopy:
                if word['ENT_LABEL'] == 'PER':
                    question = True
                    word['TOKEN'] = 'who'
            
            if question:
                out = " ".join([x['TOKEN'] for x in sentenceCopy])
                out += "?"

                output.append(out)

        return output
    
    def generateBinaryQuestions(self, taggedText):
        output = []
        for sentence in taggedText:
            sentenceCopy = deepcopy(sentence)
            question = False

            for i, word in enumerate(sentenceCopy):
                if word['LEMMA'] == 'be':
                    # FIXME: this is only gonna go back 1 word; it actually needs to go back to the head of the dependency phrase
                    sentenceCopy[i-1], sentenceCopy[i] = word, sentenceCopy[i-1]
                    question = True
            
            if question:
                out = " ".join([x['TOKEN'] for x in sentenceCopy])
                out += "?"

                output.append(out)
            
        return output            

def main():
    qg = QuestionGenerator()
    print(qg.generateWhoQuestions(tagged_text_spoof))
    print(qg.generateBinaryQuestions(tagged_text_spoof))


if __name__ == "__main__":    
    main()


