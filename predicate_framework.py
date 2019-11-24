from utils import *

class PredicateFramework:

    def __init__(self, sentence):
        # all 'find' methods assume the input to be a simple predicate
        # that is, its syntax labels are (S (NP) (VP) (.))
        # and the VP conforms to (VP (V) (NP)) or (VP (V))

        # FIXME: in passive or two-word verb constructions,
        # the predicate returned will not make sense.

        for i, child in enumerate(sentence._.children):
            if i == 0:
                self.subj = self.find_subject(child)
            
            if i == 1:
                self.verb = self.find_verb(child)
                self.obj = self.find_object(child)

    def find_subject(self, root):
        return root

    def find_verb(self, root):
        # base case: root is a verb
        if constituent_tag(root._.parse_string).startswith('VB'):
            return root

        # recursive case: find the first verb of the children
        for child in root._.children:
            cand = self.find_verb(child)
            if cand: 
                return cand

        # base case: that all failed and this predicate is a prediCANT!
        return None

    def find_object(self, root):
        print(root._.parse_string)
        if constituent_tag(root._.parse_string).startswith('N'):
            return root

        for child in root._.children:
            cand = self.find_object(child)
            if cand:
                return cand

        return None
