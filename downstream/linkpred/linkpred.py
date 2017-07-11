from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from operator import itemgetter
from time import time
import numpy as np
import multiprocessing
import random
import os
import sys

#CORES = multiprocessing.cpu_count()
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
    d[key] = map(float,val)
  f.close()
  return d

def getEdgeVector(vec1, vec2):
  #sub = np.abs(vec1 - vec2)
  #mul = vec1 * vec2
  #return np.concatenate((sub, mul), axis=0)
  return vec1 * vec2

from collections import defaultdict
def prepareDataset(data_file, data_dict):
  f = open(data_file, 'r')
  edges=[]
  g=defaultdict(lambda: defaultdict(int))
  #num_of_one_class = 5
  #count=0
  for line in f:
    arr = line.strip().split()
    id1, id2 = long(arr[0]), long(arr[1])
    edges.append([id1, id2, 1])
    g[id1][id2]=1
    #if count==num_of_one_class:
    	#break
    #count+=1
  f.close()

  nodes=g.keys()
  total=len(edges)
  for i in xrange(total):
    while True:
      n1 = nodes[random.randint(0, len(nodes)-1)]
      n2 = nodes[random.randint(0, len(nodes)-1)]
      if n1!=n2 and g[n1][n2]==0:
        edges.append([n1, n2, 0])
        break 
  data = []
  for edge in edges:
    id1, id2, label = edge[0], edge[1], edge[2]
    try:
      vec1, vec2 = np.array(data_dict[id1]), np.array(data_dict[id2])
      feature_vec = getEdgeVector(vec1, vec2)
      data.append([feature_vec, label, str(id1)+"\t"+str(id2)])
    except KeyError:
      print line
      pass
  print len(data)
  random.shuffle(data)
  tr=int(len(data)*0.7)
  rem = len(data)-tr
  train=data[0:tr]
  train_feat, train_lab, train_id  = [], [], []
  for d in train:
    #print d
    train_feat.append(d[0])
    train_lab.append(d[1])
    train_id.append(d[2])
  test=data[tr:]
  test_feat, test_lab, test_id  = [], [], []
  for d in test:
    test_feat.append(d[0])
    test_lab.append(d[1])
    test_id.append(d[2])
  return train_feat, train_lab, test_feat, test_lab, train_id, test_id

print "stating"
data_dict = loadEmbeddings(emb_f)
print "Loaded embeddings"
train_feat, train_lab, test_feat, test_lab, train_id, test_id = prepareDataset(edge_list_f, data_dict)
print "prepared dataset. starting to train"
clf = LogisticRegression()
clf.fit(train_feat,train_lab)
print "training done. starting to predict" 
lab=clf.predict(test_feat)
scores=clf.score(test_feat,test_lab)
print "done"
print(edge_list_f+"\t"+emb_f+"\t"+str(scores * 100))

print "writing output"
data = []
for i in range(len(lab)):
        arr = [str(j) for j in test_feat[i]]
        if lab[i] == test_lab[i]:
                data.append(test_id[i]+"\t"+str(1))
        else:
                data.append(test_id[i]+"\t"+str(0))


embeddingfile = sys.argv[2].strip().split("/")[-1]
graphfile = sys.argv[1].strip().split("/")[-1].split("_")[0]
outputfolder = sys.argv[3]

f=open(outputfolder+"/"+graphfile+"_"+embeddingfile+"linkpred.txt","w")
f.write("\n".join(data))
f.close()

