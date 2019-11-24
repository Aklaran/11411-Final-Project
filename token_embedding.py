# this is a word embedding module using bert

from bert_embedding import BertEmbedding
from spacy.pipeline import SentenceSegmenter
from spacy.lang.en import English
import numpy
import scipy

class BertEmbedder:

    def __init__(self, input_text):

        nlp = English()
        sentencizer = nlp.create_pipe("sentencizer")
        nlp.add_pipe(sentencizer)
        doc = nlp(input_text)
        sentences = [str(sent) for sent in doc.sents]

        bert_embedding = BertEmbedding()
        bert_embedding(sentences, 'sum')

        # list of all sentences
        self.vectorized_doc = bert_embedding(sentences)

# testing and examples
paragraph = "Islam official religion Egypt. sentence absolute gibberish. Judaism official religion Israel. Cats dogs officially best."
question1 = "official religion Egypt?"

question = question1.replace('?', '')

paragraph_vectorized = BertEmbedder(paragraph)
question_vectorized = BertEmbedder(question)

# print(len(paragraph_vectorized.vectorized_doc))

sim = []
for i in range(len(paragraph_vectorized.vectorized_doc)):
    temp_sims = []
    for q in question_vectorized.vectorized_doc[0][1]:
        max_sim = 0
        for p in paragraph_vectorized.vectorized_doc[i][1]:
            if scipy.spatial.distance.cosine(q, p) > max_sim:
                max_sim = scipy.spatial.distance.cosine(q, p)
        temp_sims.append(max_sim)
    sim.append((numpy.mean(temp_sims), i))

print(sim)

# highest_sim = max(sim, key=lambda x:x[0])[1]
# print(question1)
# print(paragraph_vectorized.vectorized_doc[highest_sim][0])


# # len 2 tuple (sentence tokens, embeddings)
# first_sentence = result[0]
# # print(len(result))

# print(first_sentence[0])
# # ['we', 'introduce', 'a', 'new', 'language', 'representation', 'model', 'called', 'bert', ',', 'which', 'stands', 'for', 'bidirectional', 'encoder', 'representations', 'from', 'transformers']
# # print(len(first_sentence))


# # tokens in first sentence
# first_sentence_tokens = first_sentence[1]

# # second token embedding in first sentence
# print(first_sentence_tokens[1])
# # array([ 0.4805648 ,  0.18369392, -0.28554988, ..., -0.01961522,
# #        1.0207764 , -0.67167974], dtype=float32)
# print(first_sentence_tokens[1].shape)
# print(first_sentence_tokens[0].shape)
# print(first_sentence_tokens[2].shape)
# # (768,)


