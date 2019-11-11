from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updatedimport os
import spacy
import string

nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated

class relevance_ranker:
    def __init__(self):
        q_file = open('togepi.txt',"r+")
        self.text = q_file.read()
        doc = nlp(self.text)
        self.tokenized_text = []
        self.sentences = [sent.string.strip() for sent in doc.sents]
        # should take in words from text and run a trigram model on the words

        # this sets up the questions
        q_file = open("Test_Q_File","r+")
        self.questions = q_file.read()
        self.q_list = self.questions.split('\n')

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
        return matches
i = relevance_ranker()
test_set = i.make_question_set(i.q_list[1])
matching_dict = i.find_best_matches(test_set)
print(max(matching_dict, key=matching_dict.get))