'''Utility functions for question asking.'''

import string

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
    return constituent_tag(span._.parse_string).startswith('VB')

def is_verb_phrase(span):
    return constituent_tag(span._.parse_string).startswith('V')

def is_noun(span):
    return constituent_tag(span._.parse_string).startswith('N')

def entity_from_span(span):
    if span._.is_coref:
        return span._.coref_cluster.main
    else:
        return span

def entity_from_span_lst(lst):
    for span in lst:
        if span._.is_coref:
            return [span._.coref_cluster.main]
    
    return lst

def str_from_token_lst(lst):
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

    return output

# Statements for debug
if __name__ == '__main__':
    print(constituent_tag('(VBZ ate)'))
    print(constituent_tag('(VP (VBZ swag) (NNP out))'))