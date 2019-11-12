from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updatedimport os
import spacy
import string

sentences= English()
nlp2 = spacy.load("en_core_web_sm")
sentences.add_pipe(sentences.create_pipe('sentencizer')) # updated

class answer_question:
    def __init__(self, text_file, question_file):
        q_file = open(text_file,"r+")
        self.text = q_file.read()
        doc = sentences(self.text)
        self.tokenized_text = []
        self.sentences = [sent.string.strip() for sent in doc.sents]

        # this sets up the questions
        q_file = open(question_file,"r+")
        self.questions = q_file.read()
        self.q_list = self.questions.split('\n')

    def make_question_set(self, question):
        q = nlp2(question)
        q_words = set(['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW', 'WHICH', '?'])
        question_vector = set()
        for word in q:
            if word.text not in q_words:
                question_vector.add(word.text.upper())
        return question_vector

    def find_best_matches(self, question_vector):
        matches = dict()
        for sentence in self.sentences:
            match_count = 0
            sentence = nlp2(sentence)
            for word in sentence:
                if word.text.upper() in question_vector:
                    match_count += 1
            match_percent = float(match_count / len(sentence))
            matches[sentence.text] = match_percent
        return max(matches, key = matches.get)

    def answer_wh_question(self, question, best_sentence):
        doc = nlp2(best_sentence)
        noun_list = []
        for token in doc:
            if token.pos_ == 'NOUN':
                noun_list.append(token.text)
        for word in noun_list:
            if word not in question:
                return word

