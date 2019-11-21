#!/usr/bin/env python3

from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updatedimport os
import spacy
import sys
import string
import preprocess as st
import ask


sentences= English()
nlp = spacy.load('en_core_web_md')
nlp2 = spacy.load("en_core_web_sm")
sentences.add_pipe(sentences.create_pipe('sentencizer')) # updated

class answer_question:
    def __init__(self, text_file, question_file):

        with open(text_file, 'r') as file:
            text = file.read()

        # Instantiate our preprocessor and get the processed doc
        preprocesser = st.Preprocessor(text)
        processed_doc = preprocesser.doc

        # Instantiate our question generator and make some questions
        question_generator = ask.QuestionGenerator()

        self.wh_questions = question_generator.generateWhQuestions(processed_doc)
        print(self.wh_questions)


        q_file = open(text_file,"r+")
        self.text = q_file.read()
        #self.text = nlp2(self.text)
        #self.text = self.text.decode('utf8').upper().encode('ascii')
        doc = sentences(self.text)
        self.tokenized_text = []
        self.sentences = [sent.string.strip() for sent in doc.sents]


        # this sets up the questions
        q_file = open(question_file,"r+")
        self.questions = q_file.read()
        #self.questions = self.questions.decode('utf8').upper().encode('ascii')
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

    def find_best_matches_vectorized(self, question):
        candidates = []
        for sent in self.wh_questions:
            candidate = nlp(str(sent))
            score = nlp(question).similarity(candidate)
            candidates.append((score, candidate))
        
        # print(candidates)
        most_similar = max(candidates, key=lambda x: x[0])
        return most_similar

    def answer_wh_question(self, question, best_sentence):
        doc = nlp2(best_sentence)
        noun_list = []
        for token in doc:
            if token.pos_ == 'NOUN':
                noun_list.append(token.text)
        for word in noun_list:
            if word not in question:
                return word
        return ""

answer_question = answer_question(sys.argv[1], sys.argv[2])

for question in answer_question.q_list:
    match = answer_question.find_best_matches_vectorized(question)


    question_vector = answer_question.make_question_set(question)
    best_matches = answer_question.find_best_matches(question_vector)
    answer = answer_question.answer_wh_question(question, best_matches)
    print(match[0], match[1], question, answer)





