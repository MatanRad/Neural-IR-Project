from gensim.models import Word2Vec
import gensim
import dataset_loader as dl
import utils
import nltk.tokenize
import _pickle as pickle
import sklearn

word_dim = 300
g_pretrain_bin_file = r"D:\IRfiles\googlenews300.bin"
outdir = r"D:\IRfiles\gensim"


''' This script counts number of words in our vocabulary for tokenized data and Google's data '''

with open("tokenized_dataset.pickle", "rb") as f:
    ids, questions, answers, all_answers = pickle.load(f)

texts = questions + all_answers


# either of these models can be used. First is Google's vocab second is our trained vocab.
#model = gensim.models.KeyedVectors.load_word2vec_format(g_pretrain_bin_file, binary=True)
model = Word2Vec.load(outdir+r"\gensim-w2v-300")

gwords = model.wv.vocab.keys()

print("google:")
print(len(model.wv.vocab.keys()))


d = {}
l = 0
for i in texts:
    for j in i:
        d[j] = 1
        l+=1


ourwords = d.keys()

# find new words in our data that are not in google's vocab
diff = [item for item in ourwords if item not in gwords]
print("diff:")
print(len(diff))

print("us:")
print(len(ourwords))
print("done")
