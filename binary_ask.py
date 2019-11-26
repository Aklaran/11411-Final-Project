#!/usr/bin/env python3
# -*- coding:utf8 -*-

import sys
import os
import string

import preprocess as st
from predicate_framework import Predicate, PredicateFinder
from qg_protocol import QuestionGenerator
from ranker import Ranker
from question import Question
from utils import * 

import pprint as pprint

import nltk
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer

pp = pprint.PrettyPrinter()

class BinaryQuestionGenerator(QuestionGenerator):

    def __init__(self):
        blockPrint()

        # this is used from the nltk library to get present tense verbs and singular nouns
        self.wnl = WordNetLemmatizer()

        enablePrint()

    def ask(self, predicates):
        output = []

        for pred in predicates:

            question = self.simple_true_predicate_q_from(pred)

            if question.is_valid():
                
                # make questions where answer is yes
                output.append(self.simple_true_predicate_q_from(pred))

        # set to remove duplicates, list to remain subscriptable
        return list(set(output))

    def simple_true_predicate_q_from(self, predicate):
        vp = str_from_token_lst(predicate.verb)
        subj = str_from_token_lst(predicate.subj)
        wh_word = predicate.wh_word
        obj = str_from_token_lst(predicate.obj)
        # TODO @amyzhang17: make a feature for predicates that can access the original text
        # after_obj = predicate.after_obj.strip()
        after_obj, raw_q = "", ""

        # raw_q = ' '.join([wh_word, vp, obj]) + '?'
        v_lemmatized = self.wnl.lemmatize(vp, 'v')
        subj_lemmatized = self.wnl.lemmatize(subj, 'n')
        if v_lemmatized != 'be':
            # example: Did Nicholas Cage steal the Declaration of Indepenedence?
            raw_q = ' '.join(['Did', subj, v_lemmatized, obj])
        else:
            # is-based verb
            if vp == 'is':
                raw_q = ' '.join(['Is', subj_lemmatized, obj])
            elif vp == 'are':
                    raw_q = ' '.join(['Are', subj, obj])
            else:
                if subj == subj_lemmatized:
                    raw_q = ' '.join(['Was', subj_lemmatized, obj])
                else:
                    raw_q = ' '.join(['Were', subj, obj])

        if len(after_obj)>0:
            raw_q += " " + after_obj
        raw_q += "?"
        question = Question(raw_q, 'BINARY', 'Yes', predicate.sentence)
        return question

# these could go in util functions
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    # Suppress printing until we show output
    # REMOVE THIS IF YOU'RE HAVING PROBLEMS
    blockPrint()

    # Ensure 2 arguments
    if len(sys.argv) != 3:
        print("Usage: ./ask ARTICLE_TXT NUM_QUESTIONS")
        sys.exit(1)

    # Read string from 1 text file. 
    # TODO: extend this to a directory of files
    INPUT_TXT = sys.argv[1]

    # validate that n_questions is an integer
    if not sys.argv[2].isdigit():
        print("NUM_QUESTIONS must be an integer")
        sys.exit(1)

    N_QUESTIONS = int(sys.argv[2])

    with open(INPUT_TXT, 'r') as file:
        text = file.read()

    # Instantiate our question generator and make some questions
    preprocessor = st.Preprocessor(text)
    doc = preprocessor.doc

    pf = PredicateFinder()
    predicates = pf.find_predicates(doc)

    question_generator = BinaryQuestionGenerator()

    binary_questions = question_generator.ask(predicates)
    
    # debug line; remove for prod
    print(len(binary_questions))
    # for question in binary_questions: 
    #     print(question.q_string)
    #     print(question.q_class)
    #     print(question.q_answer)
    #     print()

    print("RANKING")

    ranking = Ranker(binary_questions, doc)
    ranking.rank()
    ranking.sort()
    for i in range(N_QUESTIONS):
        new_question = ranking.pop_and_reinsert()
        print(new_question[0].q_string)
        print(new_question[0].q_class)
        print(new_question[0].q_answer)
        print(new_question[1])
        print()


