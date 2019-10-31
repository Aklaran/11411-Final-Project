# this is the main run file for question generation

# import Preprocessor

from copy import deepcopy

tagged_text_spoof = [[{'TOKEN': 'Trump',
                       'POS': 'NNP',
                       'ENT_LABEL': 'PER'},
                      {'TOKEN': 'is',
                       'POS': 'V',
                       'ENT_LABEL': 'NONE'},
                      {'TOKEN': 'mean',
                       'POS': 'ADJ',
                       'ENT_LABEL': 'NONE'},]]

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
                output.append(out)

        return output
                
        

def main():
    qg = QuestionGenerator()
    print(qg.generateWhoQuestions(tagged_text_spoof))


if __name__ == "__main__":    
    main()


