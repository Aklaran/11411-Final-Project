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
stopwords = spacy.lang.en.stop_words.STOP_WORDS
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
        # print(self.wh_questions)

        doc = sentences(text)
        self.sentences = [sent.string.strip() for sent in doc.sents]

        with open(question_file, 'r') as q_file:
            self.q_list = q_file.read().split('\n')

    def find_best_matches_vectorized(self, question):

        q_type = self.classify(question)

        question = nlp(question)
        question = ' '.join([token.text for token in question if not token.is_stop])
        print('STOPWORDS REMOVED: ', question)

        # generate (similarity, question) list for each question
        candidates = []
        for (sent, q_class, correct_answer) in self.wh_questions:
            og_candidate = nlp(str(sent))
            candidate = ' '.join([token.text for token in og_candidate if not token.is_stop])
            candidate = nlp(candidate)
            score = nlp(question).similarity(candidate)
            if not q_type and correct_answer:
                candidates.append((score, og_candidate, correct_answer))
            elif q_class == q_type and correct_answer:
                candidates.append((score, og_candidate, correct_answer))

        if not candidates:
            return None
        
        # return most similar candidate
        # print(sorted(candidates, key=lambda x: x[0], reverse=True)[:3])
        most_similar = max(candidates, key=lambda x: x[0])

        if most_similar[0] > 0.88:
            return most_similar
        return None

    def classify(self, question):
        types = ['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW', 'WHICH', 'BINARY']
        for t in types:
            if t in question.upper():
                return t
        return None

    def make_question_set(self, question):
        q = nlp(question)
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
            sentence = nlp(sentence)
            for word in sentence:
                if word.text.upper() in question_vector:
                    match_count += 1
            match_percent = float(match_count / len(sentence))
            matches[sentence.text] = match_percent
        return max(matches, key = matches.get)

    def answer_wh_question(self, question, best_sentence):
        doc = nlp(best_sentence)
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
    print('###### QUESTION ######')

    match = answer_question.find_best_matches_vectorized(question)
    if not match:
        match = ('Not found', 'Not found')


    question_vector = answer_question.make_question_set(question)
    best_matches = answer_question.find_best_matches(question_vector)
    answer = answer_question.answer_wh_question(question, best_matches)
    print(match[0], '\n', match[1], '\n', question, '\n', answer,'\n')





