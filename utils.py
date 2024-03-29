'''Utility functions for question asking.'''

import string
from itertools import chain

# pattern to match for simple predicates
PRED_PATTERN = ['NP', 'VP', '.']

# Wh- words corresponding to different entity types
WH_MAP = { 'PERSON': 'Who',
           'GPE': 'What',
           'LOC': 'Where',
           'ORG': 'What',
           'FC': 'What',
           'EVENT': 'What',
           'WORK_OF_ART': 'What'
         }

# Berkeley Neural Parser token tags that we will include in noun phrases
NOUN_TAGS = ['NP', 'NNP', 'NNS', 'NN', 'IN', 'POS', 'DT', 'CD', 'TO', 'PP', 'PRT', 'JJ']

VERB_TAGS = ['VBN', 'VBZ', 'VBD', 'VBP']

PERSONAL_PRONOUNS = ['HE', 'SHE', 'HIM', 'HER', 'THEY', 'THEM']

POSSESSIVES = ['HIS', 'HER', 'THEIR', 'ITS']

IMPERSONAL_PRONOUNS = ['IT']

DEMONSTRATIVES = ['THIS', 'THAT', 'THOSE', 'THESE', 'THERE']

STOP_WORDS = set(chain(PERSONAL_PRONOUNS, IMPERSONAL_PRONOUNS, DEMONSTRATIVES))

def constituent_tag(parse_string):
    '''
    The PTB tag for the given constituent.

    Parameters:
        parse_string (str): PTB-annotated constituent.

    Returns:
        tag (str): The PTB tag of the constituent.
    '''

    return parse_string.split()[0][1:]

def is_verb(span):
    # Excludes the VP (verb phrase) tag so we only get single tokens
    return constituent_tag(span._.parse_string) in VERB_TAGS

def is_verb_phrase(span):
    # Includes all possible verb phrase tags
    return constituent_tag(span._.parse_string).startswith('V')

def is_noun(span):
    return constituent_tag(span._.parse_string) in NOUN_TAGS

def entity_from_span(span):
    if span._.is_coref:
        return span._.coref_cluster.main
    else:
        return span

def entity_from_span_lst(lst):
    for span in lst:
        if span._.is_coref:
            return [span._.coref_cluster.main]
        
        for token in span:
            if token._.in_coref:
                return [token._.coref_clusters[0].main]
    
    return lst

def good_length_obj(obj):
    # a bunch of list casting cuz i'm not sure if these will be Spans or lists
    lst = list(obj)
    if len(lst) > 1:
        return True
    
    return len(list(lst[0])) > 2

def is_stop_word(word):
    return word in STOP_WORDS

def is_stop_word_or_possessive(word):
    return word in STOP_WORDS or word in POSSESSIVES

def wh_word_from(lst):
    # Get the corresponding wh word, defaults to 'What'
    # Input: list(Span)

    if len(lst) == 0 or len(lst[0]) == 0:
        return 'What'

    for span in lst:
        for token in span:
            if token.text.upper() in PERSONAL_PRONOUNS:
                return 'Who'
            
    return WH_MAP.get(lst[0][0].ent_type_, 'What')


def subj_from_token_lst(lst):
    # lowercase the subject word if it's not a proper noun
    # for use in binary questions

    first = lst[0]

    output = ''
    if not is_ent(first[0]):
        first_letter = first.text[0].lower()
        output = first_letter + first.text[1:]
    
    return str_from_token_lst(lst, output)

def is_ent(token):
    # 2 - outside ent
    # 0 - no ent tag set
    return token.ent_iob not in [0, 2]

def is_plural(span):
    return constituent_tag(span._.parse_string).endswith('S')

def str_from_token_lst(lst, first_corrected=''):
    if first_corrected != '': # subj capitalization has been fixed
        output = first_corrected
    else:
        output = lst[0].text

    num_quotes = 0

    no_space_after = set(['$', '(', '[', '{', '-'])

    no_space_before = set(string.punctuation) - set(['$', '(', '[', '{', '"'])

    for i in range(1, len(lst)):
        token = lst[i].text
        last = lst[i-1].text

        if token == '"':
            num_quotes += 1

            if num_quotes % 2 != 0:
                output += ' '

        elif last not in no_space_after and token[0] not in no_space_before:
            if last != '"' or num_quotes % 2 == 0:
                output += ' '

        output += token

    return output.strip()

# Statements for debug
if __name__ == '__main__':
    print(constituent_tag('(VBZ ate)'))
    print(constituent_tag('(VP (VBZ swag) (NNP out))'))