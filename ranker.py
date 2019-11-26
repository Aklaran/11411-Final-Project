import string
from utils import *

IDEAL_Q_LENGTH = 10
MAX_SCORE = 17

def sortSecond(val):
    return val[1]

class Ranker:
    '''
    Holds the ranking data structure for how questions are scored and sorted
    The q_list becomes a max priority queue, with the max score at the front.

    Properties:
        q_list: (list(Question, int)) list tuples of unranked questions and scores
        avg_coref_len: (int) average length of coref clusters
    '''
    
    def __init__(self, question_list, avg_coref_len):
        self.q_list = [(question, 0) for question in question_list]
        # self.doc = doc
        self.avg_coref_len = avg_coref_len
    
    def length(self):
        return len(self.q_list)

    def _rank_question(self, question):
        # is entity: +10
            # is main ref: + 5
                # ent size is large: +2
        # -abs(dist from 10 words) / 3
        score = 0
        question_ents = question.entities()
        if len(question_ents) > 0:
            score += 10
            for ent in question_ents:
                if ent == ent._.coref_cluster.main:
                    score += 5
                    if len(ent._.coref_cluster) > self.avg_coref_len:
                        score += 2
                    break
        q_len = len(question.q_string.split())
        score += (-1 * abs(q_len - IDEAL_Q_LENGTH))/3

        return score

    def rank(self):
        for i in range(len(self.q_list)):
            question = self.q_list[i][0]
            self.q_list[i] = (question, self._rank_question(question))
        

    def sort(self):
        self.q_list.sort(key = sortSecond, reverse = True) 

    def pop_and_reinsert(self):
        # pops the best question from the front of the priority queue
        # TODO @amyzhang17: currently pops the question tuple with the question and score
        # could be changed to just pop the question
        best_question = self.q_list.pop(0)
        # decrements it's score by exactly the MAX_SCORE amount
        new_worst_question = (best_question[0], best_question[1]-MAX_SCORE)
        # adds the question to the back of the priority queue (in case it needs to be reused)
        self.q_list.append(new_worst_question)
        return best_question[0]
