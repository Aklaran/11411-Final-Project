'''Helpers for finding and processing predicates.'''

from utils import *

PRED_PATTERN = ['NP', 'VP', '.']

WH_MAP = { 'PERSON': 'Who',
           'GPE': 'What',
           'LOC': 'Where',
           'ORG': 'What',
           'FC': 'What',
           'EVENT': 'What',
           'WORK_OF_ART': 'What' 
         }

class PredicateFinder:
    """Finds all the predicates in a document."""
    
    def find_predicates(self, doc):
        predicates = []

        for sentence in doc.sents:
            predicates.extend(self.find_predicates_in_sentence([], sentence))

        # for pred in predicates:
        #     print(pred.subj.text.strip(), end=' |')
        #     print(pred.wh_word)
        #     print(pred.verb)
        #     print(pred.obj)
        #     print()
        
        return predicates

    def find_predicates_in_sentence(self, predicates, root):
        # base case (also checked at every level)
        if self.is_predicate(root):
            predicates.append(Predicate(root))

        # recursive case - check children for predicates
        for child in root._.children:
            self.find_predicates_in_sentence(predicates, child)
        
        return predicates
    
    def is_predicate(self, sentence):

        for i, child in enumerate(sentence._.children):

            # handle empty label case
            if len(child._.labels) == 0:
                # if in final pos, check for period (periods have empty labels)
                if i == len(PRED_PATTERN) - 1:
                    return child.text in ['.', ',', ';', ':']

                # otherwise it's just out of place
                return False

            if child._.labels[0] != PRED_PATTERN[i]:
               return False

        # has no children - not a predicate
        return False

class Predicate:
    """
    Holds information about a predicate for easy reconstruction.
    
    Properties:
        subj: The subject of the predicate
        wh_word: the 'wh' word corresponding to the predicate's subject
        verb: The main verb of the predicate
        obj: the object of the predicate
    """

    def __init__(self, sentence):
        # all 'find' methods assume the input to be a simple predicate
        # that is, its syntax labels are (S (NP) (VP) (.))
        # and the VP conforms to (VP (V) (NP)) or (VP (V)))

        for i, child in enumerate(sentence._.children):

            if i == 0:
                self.subj = self.__find_subject(child)
                self.wh_word = self.__wh_word_from(self.subj)

            if i == 1:
                self.verb = self.__find_verb(child, [])
                self.obj = self.__find_object(child)

    def __find_subject(self, root):
        return get_entity(root)
    
    def __wh_word_from(self, span):
        return WH_MAP.get(span[0].ent_type_, 'What')

    def __find_verb(self, root, output):
        # base case: root is a verb
        if is_verb(root):
            output.append(root)

        # recursive case: find the first verb of the children
        for child in root._.children:
            if is_verb_phrase(child):
                self.__find_verb(child, output)
            else:
                return output
                
        return output

    def __find_object(self, root):
        # FIXME: prepositions and other information-holding extenders
        #        are not yet accounted for.

        print(root._.parse_string)

        # base case: root is a noun
        if is_noun(root):
            return root

        # recursive case: find the first noun in the children
        for child in root._.children:
            cand = self.__find_object(child)
            if cand:
                return cand

        # if nothing was found, could be an intransitive verb
        return None
