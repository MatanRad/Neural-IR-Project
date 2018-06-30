# PACRR Neural Net Retrieval

## Introduction

Our IR course final project.
This repository is our implementation of the PACRR network in TensorFlow.
The dataset we used is the [Yahoo! Webscope L6](https://ciir.cs.umass.edu/downloads/nfL6/) collection

#### PACRR: [arXiv:1704.03940](https://arxiv.org/abs/1704.03940)
#### Co-PACRR: [arXiv:1706.10192](https://arxiv.org/abs/1706.10192)

## General Overview

The general flow of our implementation is to load the data, tokenize it, train Google's Word2Vec model on new words, prepare epoch training data, train the network and lastly, use the pre-retrieved data from our Lucene classifier to re-rank the results using PACRR.

###### All Parameters (such as file paths) in our code will generally be at the top.

## Files

The files and their uses are listed here:
- _dataset_loader.py_ - Module for loading the data from file and pre-proccessing it. Contains the code to load files, put them in our required formats, Word2Vec the data and tokenize them (implemented in _utils.py_).
- _dataset_diff.py_ - Sample code to find how many words in our tokenized corpus are not in Google's [GoogleNews Word2Vec model](https://code.google.com/archive/p/word2vec/).
- _utils.py_ - Contains code to load general stopwords and tokenize data.
- _word2vec.py_ - Trains the Word2Vec model on new words from tokenized data.
- _prepare_epochs.ipynb_ - Jupyter Notebook to extract training data from our Word2Vec data.
- _train.ipynb_ - Jupyter Notebook to train PACRR network and save each epoch to file.
- _retrieval.ipynb_ - Jupyter Notebook to use trained network for re-ranking.

Each of these files contains its own comments on what each code-section in that file does.

## Required Modules

The following modules are required to run our PACRR code:
matplotlib, numpy, tensorflow, (optional) tensorflow-gpu, gensim, sklearn, nltk, nltk.tokenize and nltk.corpus (downloaded using nltk and python console), datetime, timeit, contextlib