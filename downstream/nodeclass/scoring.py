#!/usr/bin/env python

"""scoring.py: Script that demonstrates the multi-label classification used."""

__author__      = "Bryan Perozzi"


import numpy
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from itertools import izip
from sklearn.metrics import f1_score
from scipy.io import loadmat
from sklearn.utils import shuffle as skshuffle
from sklearn.preprocessing import MultiLabelBinarizer
import sys
from collections import defaultdict
from gensim.models import Word2Vec
from scipy.sparse import csc_matrix

class TopKRanker(OneVsRestClassifier):
    def predict(self, X, top_k_list):
        assert X.shape[0] == len(top_k_list)
        probs = numpy.asarray(super(TopKRanker, self).predict_proba(X))
        all_labels = []
        for i, k in enumerate(top_k_list):
            probs_ = probs[i, :]
            labels = self.classes_[probs_.argsort()[-k:]].tolist()
            all_labels.append(labels)
        return all_labels

def sparse2graph(x):
    G = defaultdict(lambda: set())
    cx = x.tocoo()
    for i,j,v in izip(cx.row, cx.col, cx.data):
        G[i].add(j)
    return {str(k): [str(x) for x in v] for k,v in G.iteritems()}

# 0. Files
#embeddings_file = "../wordembeddings"
#matfile = "../../data/word/POS.mat"
# load edge
#edg_file = sys.argv[1]
#lab_file = sys.argv[2]
#r = open(edg_file)
#for line in r:
#r.close()

# 1. Load Embeddings
#model = Word2Vec.load_word2vec_format(embeddings_file, binary=False) #,
                                      #norm_only=False)

# 2. Load labels
#mat = loadmat(matfile)
#A = mat['network']
#graph = sparse2graph(A)
#labels_matrix = mat['group']

# Map nodes to their features (note:  assumes nodes are labeled as integers 1:N)
#features_matrix = numpy.asarray([model[str(node)] for node in range(len(graph))])
#print(type(features_matrix[0:2]))
#print(labels_matrix.size)
#sys.exit()

lab_file = sys.argv[1] #'../graph4_labels'
embd_file = sys.argv[2] # '../wordembeddings'

#create csc matrix
le=0
r=open(lab_file, 'r')
for line in r:
    content=line.strip().split()
    for lab in content[1].split(','):
        le=le+1
r.close()
#print(le)
xrow=np.zeros(le)
xcol=np.zeros(le)
xdata=np.zeros(le)
xdata.fill(1.0)
r=open(lab_file, 'r')
c=0
mx_label=0
mx_node=0
for line in r:
    content=line.strip().split()
    x=long(content[0])#+1
    if x>mx_node:
        mx_node=x
    for lab in content[1].split(','):
        y=long(lab)
        if y>mx_label:
            mx_label=y
        xrow[c]=x
        xcol[c]=y
        c=c+1
r.close()
labels_matrix=csc_matrix((xdata, (xrow, xcol)), shape=(mx_node+1, mx_label+1), dtype=np.float32)
#print(labels_matrix.size)
'''
w=open('temp', 'w')
r=open(embd_file, 'r')
first = f.readline()
w.write(first+"\n")
for line in r:
    content=line.strip().split()
    a=long(content[0])#+1
    res=str(a)
    for b in content[1:]:
        res+=' '+b
    w.write(res+"\n")
w.close()
r.close()
'''

model = Word2Vec.load_word2vec_format(embd_file, binary=False) #,
                                      #norm_only=False)
features_matrix = numpy.asarray([model[str(node)] for node in range(mx_node+1)])
#print(type(features_matrix))
#sys.exit()

# 2. Shuffle, to create train/test groups
shuffles = []
number_shuffles = 2
for x in range(number_shuffles):
  shuffles.append(skshuffle(features_matrix, labels_matrix))

# 3. to score each train/test group
all_results = defaultdict(list)

#training_percents = [0.1, 0.5, 0.9]
training_percents = [0.7]
# uncomment for all training percents
#training_percents = numpy.asarray(range(1,10))*.1
for train_percent in training_percents:
  for shuf in shuffles:

    X, y = shuf

    training_size = int(train_percent * X.shape[0])

    X_train = X[:training_size, :]
    y_train_ = y[:training_size]

    y_train = [[] for x in xrange(y_train_.shape[0])]


    cy =  y_train_.tocoo()
    for i, j in izip(cy.row, cy.col):
        y_train[i].append(j)

    assert sum(len(l) for l in y_train) == y_train_.nnz

    X_test = X[training_size:, :]
    y_test_ = y[training_size:]

    y_test = [[] for x in xrange(y_test_.shape[0])]

    cy =  y_test_.tocoo()
    for i, j in izip(cy.row, cy.col):
        y_test[i].append(j)

    clf = TopKRanker(LogisticRegression())
    clf.fit(X_train, y_train)

    # find out how many labels should be predicted
    top_k_list = [len(l) for l in y_test]
    preds = clf.predict(X_test, top_k_list)

    results = {}
    averages = ["micro", "macro"] #, "samples", "weighted"]
    for average in averages:
        results[average] = f1_score(y_test,  preds, average=average)

    all_results[train_percent].append(results)

#print 'Results, using embeddings of dimensionality', X.shape[1]
#print '-------------------'
for train_percent in sorted(all_results.keys()):
  #print 'Train percent:', train_percent
  micro, macro=0, 0
  for x in all_results[train_percent]:
    micro+=x['micro']
    macro+=x['macro']
  micro/=len(x)
  macro/=len(x)
  print(sys.argv[1]+"\t"+sys.argv[2]+"\t"+str(micro)+"\t"+str(macro))
  #print '-------------------'
