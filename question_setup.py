import os
import spacy
import string
nlp = spacy.load('en_core_web_sm')

class question_setup:
    def __init__(self, question_file):
        q_file = open(question_file,"r+")
        self.questions = q_file.read()
        q_list = self.questions.split('\n')
        self.doc_list = []
        for question in q_list:
            self.doc_list.append(nlp(question))

        self.wh_questions = []
        self.binary_questions = []
        self.either_questions = []
        self.other_questions = []

    def canonicalize(self, question):
        q_words = set(['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW', 'WHICH'])
        for i in range(len(question)):
            if question[i].text.upper() in q_words:
                return question[i:]
        return question
        
    def classify(self, question):
        # currently only doing wh word classification
        wh_words = ['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW']
        binary_words = ['']
        for word in question:
            if word.text.upper() in wh_words:
                self.wh_questions.append(question)
                break