import os
import spacy
nlp = spacy.load('en_core_web_sm')

class QA:
    def __init__(self):
        q_file = f= open("Test_Q_File","r+")
        self.questions = q_file.read()
        self.questions = self.questions.split('\n')
        print(self.questions)

        

i = QA()