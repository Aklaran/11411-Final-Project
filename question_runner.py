from predicate_framework import PredicateFinder
from ranker import Ranker

class QuestionRunner:

    def __init__(self, doc, avg_coref_len, *generators):
        pf = PredicateFinder()
        self.predicates = pf.find_predicates(doc)

        self.avg_coref_len = avg_coref_len

        self.generators = generators

        self.questions = []

    def generate_questions(self, N, should_print=True):
        question_bins = [gen.ask(self.predicates) for gen in self.generators]

        self.save_questions(question_bins)

        rankers = [Ranker(questions, self.avg_coref_len) for questions in question_bins]

        if should_print:
            # round-robin print from ranker bins
            for i in range(N):
                j = i % len(rankers)

                question = rankers[j].pop_and_reinsert()
                print(question.q_string)

    def save_questions(self, question_bins):
        # saves all generated questions (unordered) to a property so QA can use them
 
        for questions in question_bins:
            for question in questions:
                self.questions.append(question)