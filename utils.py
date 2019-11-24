'''Utility functions for question asking.'''

def constituent_tag(parse_string):
    '''
    The PTB tag for the given constituent.

    Parameters:
        parse_string (str): PTB-annotated constituent.

    Returns:
        tag (str): The PTB tag of the constituent.
    '''

    return parse_string.split()[0][1:]

# Statements for debug
if __name__ == '__main__':
    print(constituent_tag('(VBZ ate)'))
    print(constituent_tag('(VP (VBZ swag) (NNP out))'))