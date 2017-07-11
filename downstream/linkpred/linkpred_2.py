from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from sklearn import metrics, cross_validation
from operator import itemgetter
from time import time
import numpy as np
import multiprocessing
import random
import os
import sys

CORES = multiprocessing.cpu_count()
edge_list_f = sys.argv[1]
emb_f = sys.argv[2]
random.seed(123)

# Load the full embedding file to a dict
def loadEmbeddings(path):
  f = open(path, 'r')
  first = f.readline()
  d = {}
  for line in f:
    arr = line.strip().split()
    key, val = long(arr[0]), arr[1:]
    d[key] = [float(i) for i in val]
  f.close()
  return d

def getEdgeVector(vec1, vec2):
  #sub = np.abs(vec1 - vec2)
  #mul = vec1 * vec2
  #return np.concatenate((sub, mul), axis=0)
  return vec1 * vec2

def prepareDataset(data_file, data_dict):
  f = open(data_file, 'r')
  edges=[]
  g={}
  count=1
  num_of_classes = 1000
  for line in f:
    arr = line.strip().split()
    id1, id2 = long(arr[0]), long(arr[1])
    edges.append([id1, id2, 1])
    if id1 not in g:
      g[id1]={}
    g[id1][id2]=1
    if count>=num_of_classes:
	break
    count+=1
  f.close()
  nodes=g.keys()
  total=len(edges)
  for i in xrange(total):
    while True:
      n1 = nodes[random.randint(0, len(nodes)-1)]
      n2 = nodes[random.randint(0, len(nodes)-1)]
      if n1!=n2 and n2 not in g[n1]:
        edges.append([n1, n2, 0])
        break 
  data, labels = [], []
  for edge in edges:
    id1, id2, label = edge[0], edge[1], edge[2]
    try:
      vec1, vec2 = np.array(data_dict[id1]), np.array(data_dict[id2])
      feature_vec = getEdgeVector(vec1, vec2)
      data.append(feature_vec)
      labels.append(label)
    except KeyError:
      print line
      pass
  return data, labels

print "started"
data_dict = loadEmbeddings(emb_f)
print "loaded, preparing"
X, y = prepareDataset(edge_list_f, data_dict)
print "prepared, now training"
clf = LogisticRegression(penalty='l2')
scores = cross_validation.cross_val_score(clf, X, y, cv=3, scoring='accuracy', n_jobs=1)
print(edge_list_f+"\t"+emb_f+"\t"+str(sum(scores) / len(scores) * 100))
