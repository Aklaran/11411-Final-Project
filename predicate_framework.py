'''Helpers for finding and processing predicates.'''

from utils import *

<<<<<<< Updated upstream
# pattern to match for simple predicates
PRED_PATTERN = ['NP', 'VP', '.']

# Berkeley Neural Parser token tags that we will include in noun phrases
NOUN_TAGS = ['NP', 'NNP', 'NNS', 'NN', 'IN', 'POS', 'DT', 'CD']

# Wh- words corresponding to different entity types
WH_MAP = { 'PERSON': 'Who',
           'GPE': 'What',
           'LOC': 'Where',
           'ORG': 'What',
           'FC': 'What',
           'EVENT': 'What',
           'WORK_OF_ART': 'What' 
         }

=======
>>>>>>> Stashed changes
class PredicateFinder:
    """Finds all the predicates in a document."""
    
    def find_predicates(self, doc):
        predicates = []

        for sentence in doc.sents:

            # DEBUG
<<<<<<< Updated upstream
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
=======
            print('SENTENCE:')
            print(sentence._.parse_string)
            print('\nCONSTITUENTS:')
            for child in sentence._.constituents:
                print(child._.parse_string)
                print('-')
            print('\n---\n')
            # /DEBUG

            if len(list(sentence)) <= 25:
                predicates.extend(self.find_predicates_in_sentence([], sentence))
            else: print(len(list(sentence)))

        # DEBUG
        print(len(predicates))
        for pred in predicates:
            print(pred.subj)
           # print(pred.subj_ent)
           # print(pred.wh_word)
            print(pred.verb)
            print(pred.obj)
            print()
>>>>>>> Stashed changes
        # /DEBUG

        return predicates

    def find_predicates_in_sentence(self, predicates, root):
        # base case (also checked at every level)
        if self.is_predicate(root):
            print(root)
            print(root._.parse_string)
            pred = Predicate(root)
            print(pred.subj)
            print(pred.wh_word)
            print(pred.verb)
            print(pred.obj)
            print()
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
        obj (Span): the object of the predicate
    """

    def __init__(self, sentence):
        # all 'find' methods assume the input to be a simple predicate
        # that is, its syntax labels are (S (NP) (VP) (.))
        # and the VP conforms to (VP (V) (NP)) or (VP (V))

        for i, child in enumerate(sentence._.children):

            if i == 0:
                self.subj = self.__find_subject(child, [])
                self.subj_ent = entity_from_span_lst(self.subj)
                self.wh_word = self.__wh_word_from(self.subj)
                
            if i == 1:
                self.verb = self.__find_verb(child, [])
                self.obj = self.__find_object(child)

    def __find_subject(self, root, output):
        # Recursive case: node still has children
        # Reversing the children list to prevent titles
        for child in list(root._.children)[::-1]:
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
    
    def __wh_word_from(self, lst):
        # Get the corresponding wh word, defaults to 'What'
        return WH_MAP.get(lst[0][0].ent_type_, 'What')

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

    def __find_object(self, root):
        # FIXME: prepositions and other information-holding extenders
        #        are not yet accounted for.

        # base case: root is a noun
        if is_noun(root):
            return root

        # recursive case: find the first noun in the children
        for child in root._.children:
            if is_verb(child):
                break
                
            self.__find_object(child, output)
