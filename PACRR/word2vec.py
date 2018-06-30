import os
from random import shuffle
import gensim
from gensim.models import Word2Vec
from contextlib import contextmanager
from timeit import default_timer
import datetime
import dataset_loader as dl


'''
We used Google's pre-trained GoogleNews W2V model and trained it on new words (or yahoo gibberish) from our data.
'''

word_dim = 300
g_pretrain_bin_file = r"D:\IRfiles\googlenews300.bin"
outdir = r"D:\IRfiles\gensim"
dataset_file = r"C:\Users\matan\Desktop\IR_Proj\data\anfL6.json"
tokenized_file = "tokenized_dataset.pickle"

# load our tokenized dataset
ids, questions, answers, all_answers = dl.get_dataset_tokens_loaded(dataset_file, tokenized_file)

# we want all vocabulary
alldocs = questions + all_answers

# for reshuffling per pass
doc_list = alldocs[:]

print('Input %d docs in total' % (len(doc_list)))

assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"

model = Word2Vec(size=word_dim, window=10, min_count=1, workers=32)
model.build_vocab(alldocs)
# We only want to train on new words, so intersect with google pre-trained.
model.intersect_word2vec_format(g_pretrain_bin_file, binary=True, lockf=0.0)


@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end - start


def cwidvec2str(cwid, vec):
    line = list()
    line.append(cwid)
    for idx, val in enumerate(vec):
        line.append(str(idx) + ":" + '%.6f' % val)
    return ' '.join(line)


alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes

print("START training at %s" % (datetime.datetime.now()))

for epoch in range(passes):
    shuffle(doc_list)  # shuffling gets best results
    duration = 'na'
    model.alpha, model.min_alpha = alpha, alpha
    with elapsed_timer() as elapsed:
        model.train(doc_list, total_examples=len(doc_list), epochs=model.iter)
        duration = '%.1f' % elapsed()
    print('INFO: completed pass %i at alpha %f' % (epoch + 1, alpha))
    alpha -= alpha_delta

print("INFO: all passes completed with %d terms " % len(model.wv.vocab))
if not os.path.exists(outdir):
    os.makedirs(outdir)
model.save(os.path.join(outdir, "gensim-w2v-" + str(word_dim)))

print("INFO: finished dumping %d at %s" % (word_dim, str(datetime.datetime.now())))
