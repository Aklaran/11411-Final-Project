# this is a test run of bert-as-a-service
# so far I have not gotten it to work
# (not sure how to deal with the server, and it doesn't seem like this example can be run locally)

import numpy as np
from bert_serving.client import BertClient

topk = 5

with open('Development_data/set1/set1/a1.txt') as fp:
    questions = [v.strip() for v in fp if v.strip()]
    print('%d questions loaded, avg. len of %d' % (len(questions), np.mean([len(d.split()) for d in questions])))

with BertClient(port=4000, port_out=4001) as bc:
    doc_vecs = bc.encode(questions)
    print('running')

    while True:
        query = input(('your question:'))
        query_vec = bc.encode([query])[0]
        # compute normalized dot product as score
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:topk]
        print('top %d questions similar to "%s"' % (topk, (query)))
        for idx in topk_idx:
            print('> %s\t%s' % (('%.1f' % score[idx]), (questions[idx])))