from question import Question
from qg_protocol import QuestionGenerator
from utils import str_from_token_lst

class WhQuestionGenerator(QuestionGenerator):
    def ask(self, predicates):
        output = []

        for pred in predicates:
            # make questions where answer is sentence subject
            # getting last index of verb list *probably* gets the most operant verb
            if pred.verb[-1].lemma_ == 'be':
                output.append(self.existential_q_from(pred))
            
            # make questions where answer is sentence object
            output.append(self.simple_predicate_q_from(pred))

        # set to remove duplicates, list to remain subscriptable
        output = filter(None, output) # filter out invalid questions
        return list(set(output))

    def existential_q_from(self, predicate):
        vp = str_from_token_lst(predicate.verb)
        subj = str_from_token_lst(predicate.subj)
        wh_word = predicate.wh_word
        obj = str_from_token_lst(predicate.obj)

        q_str = ' '.join([wh_word, vp, subj]) + '?'

        question = Question(q_str, wh_word.upper(), obj, predicate.sentence)
        if question.is_valid():
            return question

        return None

    def simple_predicate_q_from(self, predicate):
        vp = str_from_token_lst(predicate.verb)
        subj = str_from_token_lst(predicate.subj)
        subj_ent = str_from_token_lst(predicate.subj_ent)
        wh_word = predicate.wh_word
        obj = str_from_token_lst(predicate.obj)

        q_str = ' '.join([wh_word, vp, obj]) + '?'

        question = Question(q_str, wh_word.upper(), subj_ent, predicate.sentence)
        if question.is_valid():
            return question

        return None