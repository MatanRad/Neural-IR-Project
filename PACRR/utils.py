from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def get_stopwords():
    return set(["!!", "?!", "??", "!?", "`", "``", "''", "-lrb-", "-rrb-", "-lsb-", "-rsb-", ",", ".", ":", ";", "\"", "'", "?", "<", ">",
    "{", "}", "[", "]", "+", "-", "(", ")", "&", "%", "$", "@", "!", "^", "#", "*", "..", "...", "'ll", "'s", "'m", "a", "about", "above",
    "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
    "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours ", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
    "yours", "yourself", "yourselves", "###", "return", "arent", "cant", "couldnt", "didnt", "doesnt", "dont", "hadnt", "hasnt", "havent", "hes", "heres", "n't",
    "hows", "im", "isnt", "its", "lets", "mustnt", "shant", "shes", "shouldnt", "thats", "theres", "theyll", "theyre",
    "theyve", "wasnt", "were", "werent", "whats", "whens", "wheres", "whos", "whys", "wont", "wouldnt", "youd", "youll", "youre", "youve"] + stopwords.words('english'))


# tokenize data:
# lowercase, remove punctuation, remove stopwords (list above), remove all words appearing once
# remove empty documents.
def string_to_vec(corpus):
    stoplist = get_stopwords()
    '''for st in stoplist:
        for i in range(len(corpus)):
            corpus[i] = corpus[i].replace(st, "")'''

    texts = [[i for i in word_tokenize(doc.lower().replace(".", "").replace("(", "").replace(")", "").replace("?", "").replace(",", "").replace("-", "")) if i not in stoplist] for doc in corpus]
    #texts = [doc for doc in texts if len(doc) > 0]

    for t in texts:
        for ind, token in enumerate(t):
            if token.isdigit():
                del t[ind]


    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    return texts

