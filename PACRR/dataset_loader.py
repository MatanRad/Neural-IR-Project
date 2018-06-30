import json
import os
import _pickle as pickle
import numpy as np
import utils
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import sklearn

w2v_model = None
w2v_dict = None
w2v_path = r"D:\IRfiles\gensim\gensim-w2v-300"

#load dataset into strings
def get_dataset(file):
    with open(file, "r") as f:
        data = json.load(f)

    ids = []
    questions = []
    answers = []
    all_answers = []

    for q in data:
        ids.append(q["id"])
        questions.append(q["question"])
        answers.append(q["nbestanswers"])
        all_answers += q["nbestanswers"]

    return ids, questions, answers, all_answers


#load dataset and save it into file. if that file exists load it.
def get_dataset_loaded(file, outfile):
    if os.path.isfile(outfile):
        with open(outfile, "rb") as f:
            return pickle.load(f)
    else:
        res = get_dataset(file)
        with open(outfile, "wb") as f:
            pickle.dump(res, f)
        return res


#load dataset and tokenize it.
def get_dataset_tokens(file):
    with open(file, "r") as f:
        data = json.load(f)

    ids = []
    questions = []
    answers = []
    all_answers = []

    for q in data:
        ids.append(q["id"])
        questions.append(q["question"])

        answers_tokenized = utils.string_to_vec(q["nbestanswers"])
        answers.append(answers_tokenized)
        all_answers += answers_tokenized

    questions = utils.string_to_vec(questions)

    return ids, questions, answers, all_answers


#load dataset and tokenize it, then save to file. If that file exists load it.
def get_dataset_tokens_loaded(file, outfile):
    if os.path.isfile(outfile):
        with open(outfile, "rb") as f:
            return pickle.load(f)
    else:
        res = get_dataset_tokens(file)
        with open(outfile, "wb") as f:
            pickle.dump(res, f)
        return res


# return similarity matrix for vectors x and y
def get_cosine_mat(x, y):
    if type(x) == list:
        x = np.array(x)
        y = np.array(y)

    return sklearn.metrics.pairwise.cosine_similarity(x, y)


# given a w2v vector, change it's size to k (by padding or removing columns)
def fix_length_single(a, k):
    if len(a) > k:
        return a[:k]

    return a + [np.zeros((300)) for _ in range(k-len(a))]


# given our w2v database, fix it's length to ld and lq.
def fix_length_w2v(questions, answers, lq, ld, return_all=False):
    all_answers = []

    for i in range(len(questions)):
        questions[i] = fix_length_single(questions[i], lq)
        answers[i] = [np.array(fix_length_single(ai, ld)) for ai in answers[i]]
        if return_all:
            all_answers += answers[i]

    if return_all:
        return np.array(questions), answers, np.array(all_answers)
    else:
        return np.array(questions), answers


# initializes dictionary from strings to w2v (loads the w2v model)
def init_w2v_dict():
    global w2v_model, w2v_dict
    w2v_model = Word2Vec.load(w2v_path)
    w2v_dict = w2v_model.wv
    del w2v_model
    w2v_model = None


#converts a single array of string into array of w2v vectors.
def to_w2v(a):
    if w2v_dict is None:
        init_w2v_dict()
    #return [w2v_model[ai] for ai in a]

    for i in range(len(a)):
        a[i] = w2v_dict[a[i]]


# converts our dataset to w2v
def get_w2v_dataset(questions, answers, return_all=False):
    all_answers = []

    for i in range(len(questions)):
        to_w2v(questions[i])


        for j in range(len(answers[i])):
            to_w2v(answers[i][j])

        if return_all:
            all_answers += answers[i]

    if return_all:
        return questions, answers, all_answers
    else:
        return questions, answers


# converts only answers into w2v. (has memory optimizations (numpy arrays pre-allocated)
def get_fixed_w2v_answers(answers, ld):
    qids = []

    count = 0
    for i in answers:
        count += len(i)
    all_answers = np.empty((count, ld, 300), dtype=np.float32)

    current = 0
    for i in range(len(answers)):
        for j in range(len(answers[i])):
            to_w2v(answers[i][j])
            all_answers[current] = fix_length_single(answers[i][j], ld)
            qids.append(i)
            current += 1

    return all_answers, qids

# fixes all_answers array to specified size.
def fix_length_w2v_answers(all_answers, ld):
    for i in range(len(all_answers)):
        all_answers[i] = fix_length_single(all_answers[i], ld)

    return all_answers

# calculates histograms and sizes of all question's lengths.
def analyze_lengths(questions, all_answers):
    querylens = [len(q) for q in questions]
    answerslens = [len(a) for a in all_answers]

    querylens = np.array(querylens)
    answerslens = np.array(answerslens)

    print("query lengths: mean: %f, min: %d, max:%d, median:%f" % (
    querylens.mean(), querylens.min(), querylens.max(), np.median(querylens)))
    print("doc lengths: mean: %f, min: %d, max:%d, median:%f" % (
    answerslens.mean(), answerslens.min(), answerslens.max(), np.median(answerslens)))

    plt.title("Query lengths histogram")
    plt.hist(querylens, bins=17)
    plt.show()

    plt.title("Doc lengths histogram")
    plt.hist(answerslens, bins=50, range=(0, 50))
    plt.show()


#analyzes lengths of all questions and answers
if __name__ == '__main__':
    print("Tokenizing Dataset")

    i, q, a, al = get_dataset_tokens_loaded(r"C:\Users\matan\Desktop\IR_Proj\data\anfL6.json", "./tokenized_dataset.pickle")
    print(len(i), len(q))
    analyze_lengths(q, al)

