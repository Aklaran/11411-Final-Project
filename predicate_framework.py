from utils import *

class PredicateFramework:

    def __init__(self, sentence):
        # all 'find' methods assume the input to be a simple predicate
        # that is, its syntax labels are (S (NP) (VP) (.))
        # and the VP conforms to (VP (V) (NP)) or (VP (V))

        for i, child in enumerate(sentence._.children):
            if i == 0:
                self.subj = self.find_subject(child)
            
            if i == 1:
                self.verb = self.find_verb(child, [])
                self.obj = self.find_object(child)

    def find_subject(self, root):
        return root

    def find_verb(self, root, output):
        # base case: root is a verb
        if is_verb(root):
            output.append(root)

        # recursive case: find the first verb of the children
        for child in root._.children:
            if is_verb_phrase(child):
                self.find_verb(child, output)
            else:
                return output

        # base case: that all failed and this predicate is a prediCANT!
        return output

    def find_object(self, root):
        print(root._.parse_string)
        if is_noun(root):
            return root

        for child in root._.children:
            cand = self.find_object(child)
            if cand:
                return cand

        return None
