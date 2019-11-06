# this is a text postprocessor module, built using WordNet and pyspellchecker

from nltk.corpus import wordnet

sentence = [
    'who',
    'was',
    'a',
    'member',
    'of',
    'the',
    'group,'
    'fighting',
    'for',
    'the',
    'Spanish',
    '?'
]

syn = wordnet.synsets('fighting')

for each in syn:
    name = each.name()
    lemmas = each.lemmas()
    print(name)
    for lemma in lemmas:
        print(' ', lemma.name())