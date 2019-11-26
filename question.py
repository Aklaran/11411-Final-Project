import string
from utils import *

class Question:
    '''
    Holds data concerning a question

    Properties:
        q_string (str): The actual question
        q_class (str): The class of question (WH word or binary)
        q_answer (str): The answer to the question 
    '''
    
    def __init__(self, question, klass, answer, sentence):
        self.q_string = question
        self.q_class = klass
        self.q_answer = self.__valid_answer(answer)
        self.sentence = sentence
        self.entities = self.get_ents(sentence, [])
        print(self.q_string)
        print(self.entities)

    def is_valid(self):
        # remove punctuation
        q_str = self.q_string.translate(str.maketrans('', '', string.punctuation))

        for word in q_str.split():
            if is_stop_word(word.upper()): # upper to check with the lists in utils
                return False
        
        return True

    def __valid_answer(self, s):
        s = s.translate(s.maketrans('', '', string.punctuation))

        for word in s.split():
            if is_stop_word_or_possessive(word.upper()):
                return None

        return s

    def get_ents(self, root, output):
        for span in root._.children:
            self.get_ents(span, output)

        if len(list(root._.children)) == 0:
            if root._.is_coref:
                output.append(root._.coref_cluster.main)

        return output