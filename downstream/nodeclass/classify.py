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
from scipy import sparse

import warnings
warnings.filterwarnings("ignore")

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

labels = [line.rstrip('\n') for line in open(sys.argv[1])]
embd = [line.rstrip('\n') for line in open(sys.argv[2])][1:]

# create feature matrix
node_map = {}
seq_no = 0
node_emb_list = []
global_num_nodes = 0
for line in embd:
    content = line.strip().split()
    node_map[content[0]] = seq_no
    node_emb_list.append(content[1:])
    seq_no = seq_no + 1
    global_num_nodes = global_num_nodes + 1
# find num labels
label_map = {}
seq_no = 0
temp_num_nodes = 0
for line in labels:
    content = line.strip().split()
    if content[0] in node_map:
        for lab in content[1].split(','):
            if lab not in label_map:
                label_map[lab] = seq_no
                seq_no = seq_no + 1
        temp_num_nodes = temp_num_nodes + 1
num_labels = len(label_map)
#assert(node_emb.shape[0]!=temp_num_nodes, 'some nodes dont have labels')

# create labels matrix
label_emb_map = {} 
for line in labels:
    content = line.strip().split()
    labs = np.zeros(num_labels)
    if content[0] in node_map:
        for lab in content[1].split(','):
            labs[label_map[lab]] = 1
    	label_emb_map[node_map[content[0]]] = labs.tolist()
label_emb = []
node_emb = []
id_matrix = []
num_node_with_no_labels = 0
seq_no = 0
for node_id in xrange(global_num_nodes):
    if node_id in label_emb_map:
        label_emb.append(label_emb_map[node_id])
        node_emb.append(node_emb_list[node_id])
        id_matrix.append(seq_no)
        seq_no = seq_no + 1
    else:
        num_node_with_no_labels = num_node_with_no_labels + 1
node_emb = np.asarray(node_emb)
id_matrix = np.asarray(id_matrix)
label_emb = np.asarray(label_emb)
label_emb = sparse.csr_matrix(label_emb)
print('# nodes with no labels = '+str(num_node_with_no_labels)+' out of '+str(global_num_nodes)+' nodes')
print(id_matrix.shape)
print(label_emb.shape)
print(node_emb.shape)

# 2. Shuffle, to create train/test groups
shuffles = []
number_shuffles = 1
for x in range(number_shuffles):
  shuffles.append(skshuffle(node_emb, label_emb,id_matrix,random_state=123))

# 3. to score each train/test group
all_results = defaultdict(list)

training_percents = [0.7] #, 0.5, 0.9]
# uncomment for all training percents
#training_percents = numpy.asarray(range(1,10))*.1
for train_percent in training_percents:
  for shuf in shuffles:

    X, y,z  = shuf

    training_size = int(train_percent * X.shape[0])

    X_train = X[:training_size, :]
    y_train_ = y[:training_size]
    z_train = z[:training_size]
    y_train = [[] for x in xrange(y_train_.shape[0])]


    cy =  y_train_.tocoo()
    for i, j in izip(cy.row, cy.col):
        y_train[i].append(j)

    assert sum(len(l) for l in y_train) == y_train_.nnz

    X_test = X[training_size:, :]
    y_test_ = y[training_size:]
    z_test = z[training_size:]
    y_test = [[] for x in xrange(y_test_.shape[0])]

    cy =  y_test_.tocoo()
    for i, j in izip(cy.row, cy.col):
        y_test[i].append(j)

    clf = TopKRanker(LogisticRegression())
    #print np.isnan(X_train).any()
    #print np.isfinite(X_train).any()
    #print np.isnan(y_train).any()
    #print np.isfinite(y_train).any()
    clf.fit(X_train, y_train)

    # find out how many labels should be predicted
    top_k_list = [len(l) for l in y_test]
    preds = clf.predict(X_test, top_k_list)

    results = {}
    averages = ["micro", "macro", "samples", "weighted"]
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

data = []
for i in range(len(preds)):
        temp1 = preds[i]
        temp2 = y_test[i]
        count = len(set(temp1).intersection(set(temp2)))
        score = float(count)/len(temp1)
        data.append(str(z_test[i])+"\t"+str(score))

embeddingfile = sys.argv[2].strip().split("/")[-1]
graphfile = sys.argv[1].strip().split("/")[-1].split("_")[0]
outputfolder = sys.argv[3]

f=open(outputfolder+"/"+graphfile+"_"+embeddingfile+"classification.txt","w")
f.write("\n".join(data))
f.close()
