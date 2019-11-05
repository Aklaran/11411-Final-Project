import os
import spacy
import string
nlp = spacy.load('en_core_web_sm')

class QA:
    def __init__(self):
        q_file = f= open("Test_Q_File","r+")
        self.questions = q_file.read()
        q_list = self.questions.split('\n')
        self.doc_list = []
        for question in q_list:
            self.doc_list.append(nlp(question))
        print(self.canonicalize(self.doc_list[0]))
    def canonicalize(self, question):
        Q_Words = set(['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW',])
        for i in range(len(question)):
            print(question[i].text.upper())
            if question[i].text.upper() in Q_Words:
                return question[i:]
        return question
i = QA()