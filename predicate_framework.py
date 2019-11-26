'''Helpers for finding and processing predicates.'''

from utils import *

class PredicateFinder:
    """Finds all the predicates in a document."""
    
    def find_predicates(self, doc):
        predicates = []

        for sentence in doc.sents:

            # DEBUG
            # print('SENTENCE:')
            # print(sentence._.parse_string)
            # print('\nCONSTITUENTS:')
            # for child in sentence._.constituents:
            #     print(child._.parse_string)
            #     print('-')
            # print('\n---\n')
            # /DEBUG

            predicates.extend(self.find_predicates_in_sentence([], sentence))

        # DEBUG
        # for pred in predicates:
        #     print(pred.subj)
        #     print(pred.wh_word)
        #     print(pred.verb)
        #     print(pred.obj)
        #     print()
        # /DEBUG

        return predicates

    def find_predicates_in_sentence(self, predicates, root):
        # base case (also checked at every level)
        if self.is_predicate(root):
            # print(root)
            # print(root._.parse_string)

            pred = Predicate(root)

            # print(pred.subj)
            # print(pred.wh_word)
            # print(pred.verb)
            # print(pred.obj)
            # print(pred.is_valid())
            # print()

            if pred.is_valid():
                predicates.append(pred) 

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

            # # discard anything with more nested verbs
            # for child in child._.children:
            #     if self.has_verbs(child):
            #         return False

        # has no children - not a predicate
        return False

    # def has_verbs(self, root):
    #     if is_verb_phrase(root):
    #         return False

    #     for child in root._.children:
    #         return is_verb_phrase(child)

    #     return True

class Predicate:
    """
    Holds information about a predicate for easy reconstruction.
    
    Properties:
        subj (list(Span)): The subject of the predicate
        wh_word (str): the 'wh' word corresponding to the predicate's subject
        verb (list(Span)): The main verb of the predicate
        obj (list(Span)): the object of the predicate
    """

    def __init__(self, sentence):
        # all 'find' methods assume the input to be a simple predicate
        # that is, its syntax labels are (S (NP) (VP) (.))
        # and the VP conforms to (VP (V) (NP)) or (VP (V))
        self.sentence = sentence
        for i, child in enumerate(sentence._.children):

            if i == 0:
                self.subj = self.__find_subject(child, [])
                self.subj_ent = entity_from_span_lst(self.subj)
                self.wh_word = wh_word_from(self.subj_ent)
                
            if i == 1:
                self.verb = self.__find_verb(child, [])
                self.obj = self.__find_object(child, [])

    def is_valid(self):
        # validates that the predicate is actually a good one
        # (has a verb, has a subj, has an obj, obj isn't too short)
        return self.subj is not None and len(list(self.subj)) > 0 and \
               self.verb is not None and len(list(self.verb)) > 0 and \
               self.obj is not None and len(list(self.obj)) > 0 and \
               good_length_obj(self.obj)

    def __find_subject(self, root, output):
        # Recursive case: node still has children
        for child in list(root._.children)[::-1]: # Reversing the children list to prevent titles
            # Not adding children before a title break
            # TODO: Make this less janky
            if constituent_tag(child._.parse_string) == '_SP':
                break
            
            if is_noun(child):
                self.__find_subject(child, output)
        
        # Base case: node has no children
        if len(list(root._.children)) == 0:
            # add the token if it fits the noun pattern
            if constituent_tag(root._.parse_string) in NOUN_TAGS:
                output.append(root)
        
        # un-reverse the list
        return output[::-1]

    def __find_verb(self, root, output):
        # recursive case: find the first verb of the children
        for child in root._.children:
            # stop recursing if we hit something noun-y
            if is_noun(child):
                break
            
            self.__find_verb(child, output)

        # base case: node has no children
        if len(list(root._.children)) == 0:
            # add the token if it fits the verb pattern
            if is_verb(root):
                output.append(root)

        return output

    def __find_object(self, root, output):
        # FIXME: prepositions and other information-holding extenders
        #        are not yet accounted for.

        # Just finding the top-level NP or PP in the VP
        for child in root._.children:
            if is_noun(child):
                output.append(child)
        
        return output
